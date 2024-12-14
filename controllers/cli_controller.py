from flask import Blueprint
from init import db
from models.mission import Mission

db_commands = Blueprint("db", __name__)