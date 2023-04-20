from flask import Blueprint, render_template, redirect, request

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

    global users
    users.append({
        "nome": nome,
        "email": email,
        "senha": senha
        })
    return redirect("registrar")

@auth.route("/registrar")
def registrar():
    return render_template("auth/registrar.html")

@auth.route("/listar_usuarios")
def listar_usuarios():
    return render_template("auth/listar_usuarios.html", users=users)

@auth.route("/auth_module")
def auth_module():
    return render_template("auth/auth_module.html")