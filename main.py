#!/usr/bin/env python3.8
from website import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.views import views
from website.models import db


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # debug mode for development

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacemaker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Register the views blueprint
app.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)
