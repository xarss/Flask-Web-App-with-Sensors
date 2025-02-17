from flask import Blueprint, render_template, redirect, request, flash, url_for, session
from flask_login import login_user, login_required, logout_user
from models.auth.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth = Blueprint("auth", __name__,
                 template_folder="./views/",
                 static_folder='',
                 root_path="./")
users = []

# ------------------ Rotas ------------------ #

@auth.route("/")
def auth_index():
    return render_template("auth/auth_module.html")

@auth.route("/auth_module")
def auth_module():
    return render_template("auth/auth_module.html")

@auth.route("/login")
def login():
    return render_template("auth/login.html")

@auth.route("/registrar")
def registrar():
    return render_template("auth/registrar.html")

# Funcoes ----------------------

@auth.route("/save_user", methods=["POST"])
def save_user():
    name         = request.form['name'     ]
    username     = request.form['username' ]
    email        = request.form['email'    ]
    password     = request.form['password' ]
    cpf          = request.form['cpf'      ]
    birthDate    = request.form['birthDate']
    registerDate = datetime.now()

    user = User.insert(name=name, username=username, email=email, \
                       password=password, cpf=cpf, birthDate=birthDate, registerDate=registerDate)

    if user == "fail":
        flash("Usuário já existe")
        return redirect(url_for('auth.signup'))

    return redirect(url_for("auth.listar_usuarios"))

@auth.route("/listar_usuarios")
@login_required
def listar_usuarios():
    users = User.listUsers()
    return render_template("auth/listar_usuarios.html", users=users)


@auth.route('/login_post', methods=['POST'])
def login_post():
    email    = request.form.get('email'   )
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Falha ao logar.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('housing.view_houses'))

