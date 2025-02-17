from models.db            import db
from models.housing.house import House

class Room(db.Model):
    __tablename__ = 'rooms'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    house_id    = db.Column(db.Integer, db.ForeignKey('houses.id'))
    sensors     = db.relationship('Sensor', backref='room')
    activations = db.relationship('Activation', backref='room')

    @staticmethod
    def listSensors():
        room = Room.query.all()
        return room

    @staticmethod
    def insert(id, name):
        house = House.query.get(id)
        room = Room(name=name)
        house.rooms.append(room)
        db.session.add(room)
        db.session.commit()

    @staticmethod
    def update(id, name):
        room = Room.query.get(id)
        
        if room:
            room.name = name

        db.session.commit()

    @staticmethod
    def delete(id):
        room = Room.query.get(id)
        db.session.delete(room)
        db.session.commit()