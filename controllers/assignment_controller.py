from flask import Blueprint, request
from init import db
from models.assignments import Assignment, AssignmentSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")

# Function to get assign id
def get_assign_id(assign_id):
    stmt = db.select(Assignment).filter_by(assign_id=assign_id)
    return db.session.scalar(stmt)

# Function to send assignment not found message
def assign_not_found_message(assign_id):
    return {"message": f"Assignment with id: {assign_id} does not exist"}, 404

# Function to create or update information
def create_or_update_assign(assign, body_data):
    for attr in ["mission_id", "jet_id", "crew_id"]:
        setattr(assign, attr, body_data.get(attr, getattr(assign, attr)))
    return assign

# Read all - /assignments - GET



# Read one - /assignments/id - GET



# Create - /assignments - POST



# Update - /assignments/id - PUT and PATCH

    

# Delete - /assignments/id - DELETE