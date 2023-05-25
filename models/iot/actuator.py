from models.db import db
from models.iot.device import Device

class Actuator(db.Model):
    __tablename__ = 'actuators'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column("device_id", db.Integer(), db.ForeignKey(Device.id))
    type = db.Column(db.String(64), nullable=False)

    activations = db.relationship('Activation', backref='actuator')

    @staticmethod
    def listActuators():
        actuator = Actuator.query.all()
        return actuator

    @staticmethod
    def insert(name, description, isActive, type):
        device = Device(name=name, description=description, isActive=isActive)
        actuator = Actuator(type=type)
        device.actuators.append(actuator)
        db.session.add(device)
        db.session.commit()

    @staticmethod
    def update(id, type):
        actuator = Actuator.query.get(id)
        
        if actuator:
            actuator.type = type

        db.session.commit()

    @staticmethod
    def delete(id):
        actuator = Actuator.query.get(id)
        db.session.delete(actuator)
        db.session.commit()