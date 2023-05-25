from models.db import db
from models.iot.microcontroller import Microcontroller
from datetime import datetime

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256), nullable=False)
    dateTime = db.Column(db.DateTime, default=datetime.now())

    microcontroller_id = db.Column("microcontroller_id", db.Integer(), db.ForeignKey(Microcontroller.id))

    @staticmethod
    def listAlerts():
        alert = Alert.query.all()
        return alert

    @staticmethod
    def insert(dateTime):
        mc = Alert(dateTime=dateTime)
        db.session.add(mc)
        db.session.commit()

    @staticmethod
    def update(id, dateTime):
        alert = Alert.query.get(id)
        
        if alert:
            alert.dateTime = dateTime

        db.session.commit()

    @staticmethod
    def delete(id):
        alert = Alert.query.get(id)
        db.session.delete(alert)
        db.session.commit()