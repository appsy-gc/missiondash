from flask import Blueprint, request
from init import db
from models.crew import Crew, CrewSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

crews_bp = Blueprint("crews", __name__, url_prefix="/crews")

def get_crew_by_id(crew_id):
    stmt = db.select(Crew).filter_by(crew_id=crew_id)
    return db.session.scalar(stmt)

def crew_not_found(crew_id):
    return {"message": f"Crew name with id: {crew_id} does not exist"}, 404

# Read all - /crews - GET
@crews_bp.route("/")
def get_crews():
    stmt = db.select(Crew)
    crews_list = db.session.scalars(stmt)
    return CrewSchema(many=True).dump(crews_list)

# Read one - /crews/id - GET
@crews_bp.route("/<int:crew_id>")
def get_crew(crew_id):
    crew = get_crew_by_id(crew_id)
    if crew:
        return CrewSchema().dump(crew)
    else:
        return crew_not_found(crew_id)

# Create - /crews - POST


# Update - /crews/id - PUT and PATCH
