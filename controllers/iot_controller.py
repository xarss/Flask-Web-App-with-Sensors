from flask                      import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login                import login_required
from models.iot.actuator        import Actuator
from models.iot.sensor          import Sensor
from models.iot.device          import Device
from models.iot.read            import Read
from models.iot.microcontroller import Microcontroller
from models.housing.room        import Room
from models.db                  import db
from sqlalchemy                 import and_, asc
from models.housing.house       import House

iot = Blueprint("iot", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

# Rotas -----------------

@iot.route("/")
def iot_index():
    return render_template("/iot/iot_module.html")

"""
@iot.route("/acionamento_atuadores")
def acionamento_atuadores():
    return render_template("iot/acionamento_atuadores.html")

"""

@iot.route("/register_actuator")
def register_actuator():
    return render_template("iot/register_actuator.html")

@iot.route("/register_sensor")
def register_sensor():
    return render_template("iot/register_sensor.html")

@iot.route("/register_microcontroller")
def register_microcontroller():
    return render_template("iot/register_microcontroller.html")

# Listagens --------------------

@iot.route("/view_actuators")
def view_actuators():
    actuators = Actuator.listActuators()
    return render_template("iot/view_actuators.html", actuators=actuators)

@iot.route("/view_microcontrollers")
def view_microcontrollers():
    micros = Microcontroller.listMicrocontrollers()
    return render_template("iot/view_microcontrollers.html", micros=micros)


@iot.route("/acionamento_atuadores")
@login_required
def acionamento_atuadores():
    acts = get_actuators()
    return render_template("iot/acionamento_atuadores.html", acts=acts)

@iot.route("/get_actuators")
def get_actuators():

    results = db.session.query(
    Device.name,
    Device.description,
    Room.name.label("comodo"),
    House.name.label("casa"),
    Actuator.value
    ).join(
        Actuator, Device.id == Actuator.device_id
    ).join(
        Room, Room.id == Actuator.room_id
    ).join(
        House, House.id == Room.house_id
    ).all()

    dics = [{"name": r[0], "description": r[1], "room_name": r[2], "casa": r[3], "status": r[4]} for r in results]
    return dics



@iot.route("/view_reads")
@login_required
def view_reads():
    reads = get_reads()
    return render_template("iot/view_reads.html", reads=reads)


@iot.route("/get_reads")
def get_reads():

    results = db.session.query(
    Device.name,
    Device.description,
    Read.value,
    Read.dateTime,
    Room.name.label("comodo"),
    House.name.label("casa"),
    Sensor.measure,
    ).join(
        Sensor, Device.id == Sensor.id
    ).join(
        Read, Read.sensor_id == Sensor.id
    ).join(
        Room, Room.id == Sensor.room_id
    ).join(
        House, House.id == Room.house_id
    ).order_by(
        asc(Read.id)
    ).all()


    dics = [{"name": r[0], "description": r[1], "value": r[2], "datetime": r[3], "room_name": r[4], "casa": r[5], "measure": r[6]} for r in results]
    return dics


# Cadastros --------------

@iot.route('/save_actuator', methods=['POST'])
def save_actuator():
    name = request.form.get('name')
    tipo = request.form.get('type')
    description = request.form.get('description')
    room_id = request.form.get('room_id')

    Actuator.insert(name=name, type=tipo, description=description, isActive=True, room_id=room_id)
    return redirect(url_for('housing.view_houses'))

@iot.route('/save_microcontroller', methods=['POST'])
def save_microcontroller():
    name = request.form.get('name')
    description = request.form.get('description')
    ports = request.form.get('ports')
    isActive = request.form.get('isActive')

    isActive = True if isActive == "on" else False

    Microcontroller.insert(name=name, description=description, ports=ports, isActive=isActive)
    return redirect(url_for('iot.view_microcontrollers'))
