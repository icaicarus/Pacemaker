from wsgiref.simple_server import software_version
from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, func
from . import db

class Note(db.Model):  # define a new type of object
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # relationship between databases (one to many relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class DeviceInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_model_num = db.Column(db.Integer)
    software_version = db.Column(db.String(10000))
    dcm_serial_num = db.Column(db.Integer)
    institution_name = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # lower rate limit - number of generator pace pulses delivered per min
    lrl = db.Column(db.Integer)
    # upper rate limit - max rate at which the paced ventricular rate will track sensed atrial events
    url = db.Column(db.Integer)
    max_sensor_rate = db.Column(db.Integer)
    fixed_av_delay = db.Column(db.Integer)
    dynamic_av_delay = db.Column(db.Integer)
    sensed_av_delay_offset = db.Column(db.Integer)
    atrial_amp = db.Column(db.Integer)
    ventricular_amp = db.Column(db.Integer)
    atrial_pulse_width = db.Column(db.Integer)
    ventricular_pulse_width = db.Column(db.Integer)
    atrial_sensitivity = db.Column(db.Integer)
    ventricular_sensitivity = db.Column(db.Integer)
    vrp = db.Column(db.Integer)  # ventricular refractory period
    arp = db.Column(db.Integer)  # atrial refractory period
    pvarp = db.Column(db.Integer)  # post ventricular atrial refractory period
    pvarp_ext = db.Column(db.Integer)
    hysteresis = db.Column(db.Integer)
    rate_smoothing = db.Column(db.Integer)
    atr_duration = db.Column(db.Integer)
    atr_fallback_mode = db.Column(db.Integer)
    atr_fallback_time = db.Column(db.Integer)
    activity_threshold = db.Column(db.Integer)
    reaction_time = db.Column(db.Integer)
    # accelerometer determines the pacing rate that occurs at various levels of steady state patient activity (1 - 16)
    response_factor = db.Column(db.Integer)
    recovery_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin):  # inherit from Usermixin ONLY for the user object
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    device_information = db.relationship('DeviceInformation')
    parameters = db.relationship('Parameters')

class EgramData(db.Model):
    __tablename__ = 'egram_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    signal_value = Column(Float, nullable=False)
    event_marker = Column(String(50), nullable=True)  # Event markers: AS, AP, VS, VP

    def __init__(self, signal_value, event_marker=None):
        self.signal_value = signal_value
        self.event_marker = event_marker

class PacemakerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, status):
        self.status = status