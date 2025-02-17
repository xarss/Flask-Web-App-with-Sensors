from datetime             import datetime
from flask_sqlalchemy     import SQLAlchemy
from werkzeug.security    import generate_password_hash as hasher
from models.auth.user     import User
from models.db            import db
from models.housing.house import House
from models.housing.room  import Room
from models.iot.read      import Read
from models.iot.sensor    import Sensor
from models.iot.actuator  import Actuator


def generate_seeds(db:SQLAlchemy):
    user1 = User(
                username     = "chico",         \
                birthDate    = "2003-05-05",     \
                registerDate = "2023-03-03",      \
                cpf          = "07200112992",      \
                password     = hasher("admin"),     \
                name         = "Guilherme Schwarz",  \
                email        = "guichiwawa@gmail.com" \
            )
    
    user2 = User(
                username     = "tuzapeno",    \
                birthDate    = "2004-04-04",   \
                registerDate = "2023-03-03",    \
                cpf          = "12345678900",    \
                password     = hasher("admin"),   \
                name         = "Arthur Salerno",   \
                email        = "tuzapeno@gmail.com" \
            )
    
    user3 = User(
                username     = "thiarges",  \
                birthDate    = "2001-01-01", \
                registerDate = "2001-01-01",  \
                cpf          = "00000000001",  \
                password     = hasher("admin"), \
                name         = "Thiago Borges",  \
                email        = "thigas@gmail.com" \
            )
    
    House.insert("Minha Casa 1", "Rua da Tranquilidade")
    Room.insert(1, "Quarto 1")
    Room.insert(1, "Caixa D'agua")
    Sensor.insert("DHT22", "Temperatura: °C", True, "°C", 1)
    Sensor.insert("Sensor Boia", "Nivel: %", True, "%", 2)
    Actuator.insert("Controle Janela", "Dispositivo para controle de janelas", True, "janelasso", 1, 0)
    Actuator.insert("Controle Lâmpada", "Dispositivo para controle de lâmpadas", True, "lampadazinha", 1, 0)
    
    users = [user1, user2, user3]
    db.session.add_all( users )
    db.session.commit()