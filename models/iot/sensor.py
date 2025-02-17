from models.db         import db
from models.iot.device import Device 
from models.iot.read   import Read 

class Sensor(db.Model):
    __tablename__ = 'sensors'

    id        = db.Column("id", db.Integer, db.ForeignKey(Device.id), primary_key = True)
    measure   = db.Column(db.String(64), nullable=False)
    reads     = db.relationship("Read", backref="sensors", lazy=True)
    room_id   = db.Column("room_id", db.Integer(), db.ForeignKey("rooms.id"))

    @staticmethod
    def listSensors():
        sensors = Sensor.query.join(Device, Device.id == Sensor.id).add_columns(Sensor.id, Device.name, Sensor.measure, Device.description, Device.isActive).all()
        return sensors

    @staticmethod
    def insert(name, description, isActive, measure, room_id):
        sensor = Sensor(measure=measure, room_id=room_id)
        device = Device(name=name, description=description, isActive=isActive)
        read   = Read(id=sensor.id, value=0)
        sensor.reads.append(read)
        device.sensors.append(sensor)
        db.session.add(device)
        db.session.commit()

    @staticmethod
    def insertRead(id, value):
        sensor = Sensor.query.get(id)
        
        if sensor.reads:
            read = sensor.reads[0]
            read.value = value
        else:
            read = Read(value=value)
            sensor.reads.append(read)
            db.session.add(read)

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