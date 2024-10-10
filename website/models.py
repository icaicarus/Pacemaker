from wsgiref.simple_server import software_version
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):  # define a new type of object
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #relationship between databases (one to many relationship)

class DeviceInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_model_num = db.Column(db.Integer)
    software_version = db.Column(db.String(10000))
    dcm_serial_num = db.Column(db.Integer)
    institution_name = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):  # inherit from Usermixin ONLY for the user object
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    device_information = db.relationship('DeviceInformation')

