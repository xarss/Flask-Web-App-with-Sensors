from models.db import db

class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    isActive = db.Column(db.Boolean, default=False)

    microcontrollers = db.relationship('Microcontroller', backref='devices', lazy=True)
    sensors = db.relationship('Sensor', backref='devices', lazy=True)
    actuators = db.relationship('Actuator', backref='devices', lazy=True)

    @staticmethod
    def listSensors():
        device = Device.query.all()
        return device

    @staticmethod
    def insert(name, description, isActive):
        device = Device(name=name, description=description, isActive=isActive)
        db.session.add(device)
        db.session.commit()

    @staticmethod
    def update(id, name, description, isActive):
        device = Device.query.get(id)
        
        if device:
            device.name        = name
            device.description = description
            device.isActive    = isActive

        db.session.commit()

    @staticmethod
    def delete(id):
        device = Device.query.get(id)
        db.session.delete(device)
        db.session.commit()