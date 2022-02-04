
import json
from cgitb import handler
from re import S
from sqlite3 import IntegrityError
from typing import Type, final
from flask import Flask, Response, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///game.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)


@app.route("/test/")
def testi():
    return "Moro"
