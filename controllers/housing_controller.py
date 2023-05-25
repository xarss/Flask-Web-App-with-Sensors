from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models.housing.house import House
from models.housing.room import Room
from models.db import db

housing = Blueprint("housing", __name__, template_folder = './views/', static_folder='./static/', root_path="./")

# ------------- Rotas ------------- #

@housing.route("/")
def housing_index():
    return render_template("/housing/housing_index.html")

@housing.route("/register_house")
@login_required
def register_house():
    return render_template("housing/register_house.html")

@housing.route("/register_room")
@login_required
def register_room():
    return render_template("housing/register_room.html")

# ------------ Listagens ------------ #

@housing.route("/view_houses")
@login_required
def view_houses():
    houses = House.query.all()
    return render_template("housing/view_houses.html", houses=houses)

@housing.route("/view_rooms")
@login_required
def view_rooms():
    rooms = Room.query.all()
    return render_template("housing/view_rooms.html", rooms=rooms)

# ------------- Cadastros ------------- #

@housing.route('/save_house', methods=['POST'])
def save_house():
    name = request.form.get('name')
    address = request.form.get('address')
    House.insert(name=name, address=address)
    return redirect(url_for('admin.housing.view_houses'))

@housing.route('/save_room', methods=['POST'])
def save_room():
    name = request.form.get('name')
    Room.insert(name=name)
    return redirect(url_for('admin.housing.view_rooms'))