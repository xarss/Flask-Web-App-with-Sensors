from models.db import db
from models.iot.sensor import Sensor
from models.housing.room import Room
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'reads'

    id        = db.Column( db.Integer, primary_key=True       )
    value     = db.Column(   db.Float, nullable=False         )
    dateTime  = db.Column(db.DateTime, default=datetime.now())

    room_id = db.Column("room_id", db.Integer(), db.ForeignKey(Room.id))
    sensor_id = db.Column("sensor_id", db.Integer(), db.ForeignKey(Sensor.id), nullable=False)

    @staticmethod
    def listSensors():
        reads = Read.query.all()
        return reads

    @staticmethod
    def insert(value, dateTime):
        read = Read(value=value, dateTime=dateTime)
        db.session.add(read)
        db.session.commit()

    @staticmethod
    def update(id, value, dateTime):
        read = Read.query.get(id)
        
        if read:
            read.value    = value
            read.dateTime = dateTime

        db.session.commit()

    @staticmethod
    def delete(id):
        read = Read.query.get(id)
        db.session.delete(read)
        db.session.commit()