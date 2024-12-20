from flask import Blueprint, request
from init import db
from models.assignments import Assignment, AssignmentSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")

# Function to get assign id
def get_assign_id(assign_id):
    stmt = db.select(Assignment).filter_by(assign_id=assign_id).order_by(Assignment.assign_id)
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
@assignments_bp.route("/")
def get_assignments():
    stmt = db.select(Assignment).order_by(Assignment.assign_id)
    assignments_list = db.session.scalars(stmt)
    return AssignmentSchema(many=True).dump(assignments_list)


# Read one - /assignments/id - GET
@assignments_bp.route("/<int:assign_id>")
def get_assignment(assign_id):
    assignment = get_assign_id(assign_id)
    if not assignment:
        return assign_not_found_message(assign_id)
    return AssignmentSchema().dump(assignment)


# Create - /assignments - POST
@assignments_bp.route("/", methods=["POST"])
def create_assignment():
    try:
        body_data = AssignmentSchema().load(request.get_json())
        new_assignment = create_or_update_assign(Assignment(), body_data)
        db.session.add(new_assignment)
        db.session.commit()
        return AssignmentSchema().dump(new_assignment)
    except ValidationError as err:
        # Catch and handle validation errors
        return {"message": err.messages}, 400    
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409


# Update - /assignments/id - PUT and PATCH
@assignments_bp.route("/<int:assign_id>", methods=["PUT", "PATCH"])
def update_assignment(assign_id):
    assignment = get_assign_id(assign_id)
    if not assignment:
        return assign_not_found_message(assign_id)
    body_data = AssignmentSchema().load(request.get_json(), partial=True)
    updated_assignment = create_or_update_assign(assignment, body_data)
    db.session.commit()
    return AssignmentSchema().dump(updated_assignment)
    
    

# Delete - /assignments/id - DELETE
@assignments_bp.route("/<int:assign_id>", methods=["DELETE"])
def delete_assignment(assign_id):
    assignment = get_assign_id(assign_id)
    if not assignment:
        return assign_not_found_message(assign_id)
    db.session.delete(assignment)
    db.session.commit()
    return {"message": f"Assignment with id: '{assign_id}' successfully deleted"}