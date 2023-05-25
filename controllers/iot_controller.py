from flask import Blueprint, render_template, request, url_for, redirect
from models.iot.actuator import Actuator
from models.iot.sensor import Sensor
from models.iot.microcontroller import Microcontroller

iot = Blueprint("iot", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

# Rotas -----------------

@iot.route("/")
def iot_index():
    return render_template("/iot/iot_module.html")

@iot.route("/acionamento_sensores")
def acionamento_sensores():
    return render_template("iot/acionamento_sensores.html")

# Listagens --------------------

@iot.route("/view_actuators")
def view_actuators():
    actuators = Actuator.listActuators()
    return render_template("iot/view_actuators.html", actuators=actuators)

@iot.route("/view_sensors")
def view_sensors():
    sensors = Sensor.listSensors()
    return render_template("iot/view_sensors.html", sensors=sensors)

@iot.route("/view_microcontrollers")
def view_microcontrollers():
    micros = Microcontroller.listMicrocontrollers()
    return render_template("iot/view_microcontrollers.html", micros=micros)

# Cadastros --------------

@iot.route('/save_actuator', methods=['POST'])
def save_actuator():
    name = request.form.get('name')
    tipo = request.form.get('type')
    description = request.form.get('description')
    isActive = request.form.get('isActive')
    Actuator.insert(name=name, type=tipo, description=description, isActive=isActive)
    return redirect(url_for('admin.iot.view_actuators'))

@iot.route('/save_sensor', methods=['POST'])
def save_sensor():
    name = request.form.get('name')
    description = request.form.get('description')
    measure = request.form.get('measure')
    isActive = request.form.get('isActive')
    Sensor.insert(name=name, description=description, measure=measure, isActive=isActive)
    return redirect(url_for('admin.iot.view_sensors'))

@iot.route('/save_microcontroller', methods=['POST'])
def save_microcontroller():
    name = request.form.get('name')
    description = request.form.get('description')
    ports = request.form.get('ports')
    isActive = request.form.get('isActive')
    Microcontroller.insert(name=name, description=description, ports=ports, isActive=isActive)
    return redirect(url_for('admin.iot.view_microcontrollers'))