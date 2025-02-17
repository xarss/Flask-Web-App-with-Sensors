from models.db import db
from models.housing.room import Room
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'reads'

    id        = db.Column( db.Integer, primary_key=True       )
    value     = db.Column(   db.Float, nullable=False         )
    dateTime  = db.Column(db.DateTime, default=datetime.now())
    sensor_id = db.Column("sensor_id", db.Integer(), db.ForeignKey("sensors.id"), nullable=False)

    @staticmethod
    def listReads():
        reads = Read.query.all()
        return reads

    @staticmethod
    def insert(value):
        read = Read(value=value)
        db.session.add(read)
        db.session.commit()

    @staticmethod
    def update(id, value):
        read = Read.query.get(id)
        
        if read:
            read.value    = value
            read.dateTime = datetime.now()

        db.session.commit()

    @staticmethod
    def delete(id):
        read = Read.query.get(id)
        db.session.delete(read)
        db.session.commit()