from flask import Blueprint, request
from init import db
from models.crew import Crew, CrewSchema, crews_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

crews_bp = Blueprint("crews", __name__, url_prefix="/crews")

def get_crew_by_id(crew_id):
    stmt = db.select(Crew).filter_by(crew_id=crew_id)
    return db.session.scalar(stmt)

def crew_not_found(crew_id):
    return {"message": f"Crew name with id: {crew_id} does not exist"}, 404

# Function to create or update information
def create_or_update_crew(crew, body_data):
    crew.name = body_data.get("name", crew.name)
    return crew

# Read all - /crews - GET
@crews_bp.route("/", methods=["GET"])
def get_crews():
    stmt = db.select(Crew).order_by(Crew.crew_id)
    crews_list = db.session.scalars(stmt)
    return crews_schema.dump(crews_list), 200

# Read one - /crews/id - GET
@crews_bp.route("/<int:crew_id>", methods=["GET"])
def get_crew(crew_id):
    crew = get_crew_by_id(crew_id)
    if not crew:
        return crew_not_found(crew_id)
    return CrewSchema().dump(crew)

# Create - /crews - POST
@crews_bp.route("/", methods=["POST"])
def create_crew():
    try:
        # Get information from request body
        body_data = CrewSchema().load(request.get_json())
        # Create crew instance
        new_crew = create_or_update_crew(Crew(), body_data)
        # Add new crew and commit
        db.session.add(new_crew)
        db.session.commit()
        return CrewSchema().dump(new_crew)
    except ValidationError as err:
        # Catch and handle validation errors
        return {"message": err.messages}, 400    
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            name = body_data.get("name", "unknown")
            return {"message": f"Crew with name: '{name}' already exists"}, 409
        return {"message": "An unexpected database error occurred."}, 500


# Update - /crews/id - PUT and PATCH
@crews_bp.route("/<int:crew_id>", methods=["PUT", "PATCH"])
def update_crew(crew_id):
    crew = get_crew_by_id(crew_id)
    if not crew:
        return crew_not_found(crew_id)
    body_data = CrewSchema().load(request.get_json())
    updated_crew = create_or_update_crew(crew, body_data)
    db.session.commit()
    return CrewSchema().dump(updated_crew)

# Delete - /crews/id - DELETE
@crews_bp.route("/<int:crew_id>", methods=["DELETE"])
def delete_crew(crew_id):
    crew = get_crew_by_id(crew_id)
    if not crew:
        return crew_not_found(crew_id)
    db.session.delete(crew)
    db.session.commit()
    return {"message": f"Crew with name: '{crew.name}' successfuly deleted"}