from flask import Blueprint, render_template, redirect, request, flash, url_for
from models.db import db
from models.auth.user import User
from werkzeug.security import generate_password_hash

auth = Blueprint("auth", __name__,
                 template_folder="./views/",
                 static_folder='./static/',
                 root_path="./")
users = []

@auth.route("/")
def auth_index():
    return render_template("auth/auth_module.html")

@auth.route("/login")
def login():
    return render_template("auth/login.html")

@auth.route("/post-user", methods=["POST"])
def post_user():
    '''Gets values from login.html form'''
    nome  = request.form['nome' ]
    email = request.form['email']
    senha = request.form['senha']

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email já existe")
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username=nome, password=generate_password_hash(senha, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect("registrar")

@auth.route("/registrar")
def registrar():
    return render_template("auth/registrar.html")

@auth.route("/listar_usuarios")
def listar_usuarios():
    users = User.listUsers()
    return render_template("auth/listar_usuarios.html", users=users)

@auth.route("/auth_module")
def auth_module():
    return render_template("auth/auth_module.html")