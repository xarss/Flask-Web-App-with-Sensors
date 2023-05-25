from models.db import db
from models.auth.user import User
from werkzeug.security import generate_password_hash as hasher
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def generate_seeds(db:SQLAlchemy):
    user1 = User(
                username     = "chico",         \
                birthDate    = "05-16-2003",     \
                registerDate = "25-05-2023",      \
                cpf          = "07200112992",      \
                password     = hasher("admin"),     \
                name         = "Guilherme Schwarz",  \
                email        = "guichiwawa@gmail.com" \
            )
    
    user2 = User(
                username     = "tuzapeno",    \
                birthDate    = "02-11-2004",   \
                registerDate = "25-05-2023",    \
                cpf          = "12345678900",    \
                password     = hasher("admin"),   \
                name         = "Arthur Salerno",   \
                email        = "tuzapeno@gmail.com" \
            )
    
    user3 = User(
                username     = "thiarges",  \
                birthDate    = "01-01-2001", \
                registerDate = "01-01-2001",  \
                cpf          = "00000000001",  \
                password     = hasher("admin"), \
                name         = "Thiago Borges",  \
                email        = "thigas@gmail.com" \
            )
    
    users = [user1, user2, user3]

    db.session.add_all( users )
    db.session.commit()