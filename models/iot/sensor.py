from models.db         import db
from models.iot.device import Device 

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id = db.Column("id", db.Integer, db.ForeignKey(Device.id), primary_key = True)
    measure = db.Column(db.String(64), nullable=False)
    reads = db.relationship("Read", backref="sensors", lazy=True)

    @staticmethod
    def listSensors():
        sensors = Sensor.query.all()
        return sensors

    @staticmethod
    def insert(name, description, isActive, measure):
        sensor = Sensor(measure=measure)
        device = Device(name=name, description=description, isActive=isActive)
        device.sensors.append(sensor)
        db.session.add(device)
        db.session.commit()

    @staticmethod
    def update(id, measure):
        sensor = Sensor.query.get(id)
        
        if sensor:
            sensor.measure = measure

        db.session.commit()

    @staticmethod
    def delete(id):
        sensor = Sensor.query.get(id)
        db.session.delete(sensor)
        db.session.commit()