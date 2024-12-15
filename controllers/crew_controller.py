from flask import Blueprint, request
from init import db
from models.crew import Crew, CrewSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

crews_bp = Blueprint("crews", __name__, url_prefix="/crews")

# Read all - /crews - GET
@crews_bp.route("/")
def get_crews():
    stmt = db.select(Crew)
    crews_list = db.session.scalars(stmt)
    return CrewSchema(many=True).dump(crews_list)

# Read one - /crews/id - GET


# Create - /crews - POST


# Update - /crews/id - PUT and PATCH
