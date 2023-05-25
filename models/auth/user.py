from models.db import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column("id",  db.Integer(), primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    birthDate = db.Column(db.Date, nullable=False)
    registerDate = db.Column(db.Date, default=datetime.now())

    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False) 
    
    @staticmethod
    def listUsers():
        users = User.query.all()
        return users

    @staticmethod
    def insert(name, cpf, birthDate, registerDate, username, email, password):

        check_cpf =      User.query.filter_by(cpf=cpf).first()
        check_username = User.query.filter_by(username=username).first()
        check_email =    User.query.filter_by(email=email).first()

        if not all([check_cpf, check_username, check_email]):
            user = User(name=name, cpf=cpf, birthDate=birthDate,\
                            registerDate=registerDate, username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return
        return "fail"

    @staticmethod
    def update(name, cpf, birthDate, registerDate, username, email, password):
        user = User.query.get(cpf)
        
        if user:
            user.name = name
            user.cpf = cpf
            user.birthDate = birthDate
            user.registerDate = registerDate
            user.username = username
            user.email = email
            user.password = password

        db.session.commit()

    @staticmethod
    def delete(cpf):
        user = User.query.get(cpf)
        db.session.delete(user)
        db.session.commit()