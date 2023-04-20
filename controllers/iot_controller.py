from flask import Blueprint, render_template

iot = Blueprint("iot", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

@iot.route("/")
def iot_index():
    return render_template("/iot/iot_module.html")

@iot.route("/acionamento_sensores")
def acionamento_sensores():
    return render_template("iot/acionamento_sensores.html")