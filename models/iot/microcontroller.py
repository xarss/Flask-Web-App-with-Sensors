from models.db import db
from models.iot.device import Device

class Microcontroller(db.Model):
    __tablename__ = 'microcontrollers'

    id = db.Column("microcontroller_id", db.Integer(), db.ForeignKey(Device.id), primary_key=True)
    ports = db.Column(db.Integer, nullable=False)
    
    alerts = db.relationship("Alert", backref="microcontrollers", lazy=True)


    @staticmethod
    def listMicrocontrollers():
        mc = Microcontroller.query.join(Device, Device.id == Microcontroller.id).add_columns(Device.name, Device.description, Device.isActive, Microcontroller.ports).all()
        return mc

    @staticmethod
    def insert(name, description, isActive, ports):
        device = Device(name=name, description=description, isActive=isActive)
        micro = Microcontroller(ports=ports)
        device.microcontrollers.append(micro)
        db.session.add(device)
        db.session.commit()

    @staticmethod
    def update(id, ports):
        mc = Microcontroller.query.get(id)
        
        if mc:
            mc.ports = ports

        db.session.commit()

    @staticmethod
    def delete(id):
        mc = Microcontroller.query.get(id)
        db.session.delete(mc)
        db.session.commit()