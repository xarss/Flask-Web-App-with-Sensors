from models.db import db
from datetime  import datetime
from models.iot.device import Device


class Activation(db.Model):
    __tablename__ = 'activations'

    id          = db.Column(db.Integer(), db.ForeignKey(Device.id), primary_key=True)
    dateTime    = db.Column(db.DateTime, default=datetime.now()      )

    room_id     = db.Column( db.Integer, db.ForeignKey(    'rooms.id'))
    actuator_id = db.Column( db.Integer, db.ForeignKey('actuators.id'))

    @staticmethod
    def listSensors():
        activation = Activation.query.all()
        return activation

    @staticmethod
    def insert(name, dateTime):
        activation = Activation(dateTime=dateTime)
        db.session.add(activation)
        db.session.commit()

    @staticmethod
    def update(id, dateTime):
        activation = Activation.query.get(id)
        
        if activation:
            activation.dateTime = dateTime

        db.session.commit()

    @staticmethod
    def delete(id):
        activation = Activation.query.get(id)
        db.session.delete(activation)
        db.session.commit()
