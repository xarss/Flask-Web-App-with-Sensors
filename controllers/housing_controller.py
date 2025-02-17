from flask                import Blueprint, render_template, request, redirect, url_for
from flask_login          import login_required
from models.housing.house import House
from models.housing.room  import Room
from models.iot.sensor    import Sensor
from models.db            import db
from models.iot.device    import Device
from models.iot.actuator  import Actuator

housing = Blueprint("housing", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

# ------------- Rotas ------------- #

@housing.route("/")
def housing_index():
    return render_template("housing/housing_module.html")


@housing.route("/register_house")
@login_required
def register_house():
    return render_template("housing/register_house.html")

@housing.route("/register_room", methods=['POST'])
@login_required
def register_room():
    house_id = request.form.get('house_id')
    return render_template("housing/register_room.html", house_id=house_id)

# ------------ Listagens ------------ #

@housing.route("/view_houses")
@login_required
def view_houses():
    houses = House.query.all()
    return render_template("housing/view_houses.html", houses=houses)

@housing.route("/view_rooms", methods=['POST', 'GET'])
@login_required
def view_rooms():
    house_id = request.form.get('house_id')
    rooms = Room.query.filter_by(house_id=house_id).all()
    return render_template("housing/view_rooms.html", rooms=rooms)
    

@housing.route("/view_room_sensors", methods=['POST', 'GET'])
def view_room_sensors():
    room_id = request.form.get('room_id')

    if room_id:
        sensors = db.session.query(Device).join(Sensor).filter(Sensor.room_id == room_id).all()
        return render_template("housing/view_room_sensors.html", sensors=sensors)
    
    room_id = request.args.get('room_id')
    sensors = db.session.query(Device).join(Sensor).filter(Sensor.room_id == room_id).all()
    return render_template("housing/view_room_sensors.html", sensors=sensors)

@housing.route("/view_room_actuators", methods=['POST', 'GET'])
def view_room_actuators():
    room_id = request.form.get('room_id')

    if room_id:
        actuators = db.session.query(Device).join(Actuator).filter(Actuator.room_id == room_id).all()
        return render_template("housing/view_room_actuators.html", actuators=actuators)
    
    room_id = request.args.get('room_id')
    actuators = db.session.query(Device).join(Actuator).filter(Actuator.room_id == room_id).all()
    return render_template("housing/view_room_actuators.html", actuators=actuators)

    


# ------------- Cadastros ------------- #

@housing.route('/save_house', methods=['POST'])
def save_house():
    name = request.form.get('name')
    address = request.form.get('address')
    House.insert(name=name, address=address)
    return redirect(url_for('housing.view_houses'))

@housing.route('/save_room', methods=['POST'])
def save_room():
    name = request.form.get('name')
    house_id = request.form.get('house_id')
    Room.insert(name=name, id=house_id)
    return redirect(url_for('housing.view_houses'))
                 
@housing.route('/redirect_register_room', methods=['POST'])
def redirect_register_room():
    house_id = request.form.get('house_id')
    return render_template("housing/register_room.html", house_id = house_id)

@housing.route('/register_sensor_room', methods=['POST'])
def register_sensor_room():
    room_id = request.form.get('room_id')
    return render_template("housing/register_sensor.html", room_id=room_id)

@housing.route('/register_actuator_room', methods=['POST'])
def register_actuator_room():
    room_id = request.form.get('room_id')
    return render_template("housing/register_actuator.html", room_id=room_id)

@housing.route('/save_sensor', methods=['POST'])
def save_sensor():
    name = request.form.get('name')
    description = request.form.get('description')
    measure = request.form.get('measure')
    isActive = request.form.get('isActive')
    room_id = request.form.get('room_id')

    isActive = True if isActive == "on" else False

    Sensor.insert(name=name, description=description, measure=measure, isActive=isActive, room_id=room_id)
    return redirect(url_for('housing.view_room_sensors', room_id=room_id))
