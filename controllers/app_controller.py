from flask                            import Flask, render_template, request
from models.db                        import db, instance
from controllers.iot_controller       import iot
from controllers.auth_controller      import auth
from controllers.housing_controller   import housing
from flask_login                      import LoginManager
from flask_mqtt                       import Mqtt
from flask_socketio                   import SocketIO
from flask_bootstrap                  import Bootstrap
from models.iot.sensor                import Sensor
from models.iot.actuator              import Actuator
import json

mqtt = Mqtt()

def create_app() -> Flask:
    app = Flask(__name__, template_folder="./views/", 
                        static_folder="./static/", 
                        root_path="./")

    

    app.config["TESTING"   ] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    db.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    mqtt.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models.auth.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(auth   , url_prefix = '/auth'   )
    app.register_blueprint(iot    , url_prefix = '/iot'    )
    app.register_blueprint(housing, url_prefix = '/housing')

    @app.route('/')
    def index():
        return render_template("home.html")
    
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):    
        mqtt.subscribe('iot/temperatura')
        mqtt.subscribe('iot/nivelagua')
        

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=json.loads(message.payload.decode())
        )
        with app.app_context():
            if data['topic'] == "iot/temperatura":
                Sensor.insertRead(1, float(data['payload']['temperature']))
            
            if data['topic'] == "iot/nivelagua":
                Sensor.insertRead(2, float(data['payload']['nivel']))
            
    @app.route('/publish_janela')
    def publish_janela():
        actuator = db.session.query(Actuator).filter(Actuator.id == 1).first()

        if actuator.value == 0:
            status = 1
        else:
            status = 0

        actuator.value = status
        db.session.commit()

        mqtt.publish('iot/janela', status)
        return "Message published"
    
    @app.route('/publish_lampada')
    def publish_lampada():
        actuator = db.session.query(Actuator).filter(Actuator.id == 2).first()

        if actuator.value == 0:
            status = 1
        else:
            status = 0

        actuator.value = status
        db.session.commit()

        mqtt.publish('iot/lampada', status)
        return "Message published"

    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)



    return app