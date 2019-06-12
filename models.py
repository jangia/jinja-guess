import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "postgres://svfcasbrkfdcow:600fc46d0c843ba4818b7a7f422d10785890950b82fd9c3d802eb89ce54b8fcd@ec2-79-125-4-72.eu-west-1.compute.amazonaws.com:5432/dfs70agbsg1d5n"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    secret_number = db.Column(db.Integer)