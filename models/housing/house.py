from models.db import db

class House(db.Model):
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)

    rooms = db.relationship('Room', backref='houses')

    @staticmethod
    def listSensors():
        houses = House.query.all()
        return houses

    @staticmethod
    def insert(name, address):
        house = House(name=name, address=address)
        db.session.add(house)
        db.session.commit()

    @staticmethod
    def update(id, name, address):
        house = House.query.get(id)
        
        if house:
            house.name    = name
            house.address = address

        db.session.commit()

    @staticmethod
    def delete(id):
        house = House.query.get(id)
        db.session.delete(house)
        db.session.commit()