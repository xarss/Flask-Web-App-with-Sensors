from flask                       import Flask, render_template
from models.db                   import db, instance
from controllers.iot_controller  import iot
from controllers.auth_controller import auth
from flask_login                 import LoginManager

def create_app() -> Flask:
    app = Flask(__name__, template_folder="./views/", static_folder="./static/")

    app.config["TESTING"] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(auth, url_prefix = '/auth')
    app.register_blueprint( iot, url_prefix =  '/iot')

    @app.route('/')
    def index():
        return render_template("home.html")
    
    return app