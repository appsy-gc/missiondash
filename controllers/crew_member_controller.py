from flask import Blueprint, request
from init import db
from models.crew_member import CrewMember, CrewMemberSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

crew_members_bp = Blueprint("crew_members", __name__, url_prefix="/crew_members")

# Function to get crew_member id
def get_crew_member_id(crew_member_id):
    stmt = db.select(CrewMember).filter_by(crew_member_id=crew_member_id)
    return db.session.scalar(stmt)

# Function to send crew member not found message
def crew_member_not_found_message(crew_member_id):
    return {"message": f"Crew member with id: {crew_member_id} does not exist"}, 404

# Function to create or update information
def create_or_update_crew_member(crew_member, body_data):
    for attr in ["crew_id", "name", "role", "availability"]:
        setattr(crew_member, attr, body_data.get(attr, getattr(crew_member, attr)))
    return crew_member

# Read all - /crew_members - GET
@crew_members_bp.route("/", methods=["GET"])
def get_crew_members():
    stmt = db.select(CrewMember).order_by(CrewMember.crew_member_id)
    crew_members_list = db.session.scalars(stmt)
    return CrewMemberSchema(many=True).dump(crew_members_list)


# Read one - /crew_members/id - GET
@crew_members_bp.route("/<int:crew_member_id>", methods=["GET"])
def get_crew_member(crew_member_id):
    crew_member = get_crew_member_id(crew_member_id)
    if not crew_member:
        return crew_member_not_found_message(crew_member_id)
    return CrewMemberSchema().dump(crew_member)


# Create - /crew_members - POST
@crew_members_bp.route("/", methods=["POST"])
def create_crew_member():
    try:
        # Get information from request body
        body_data = CrewMemberSchema().load(request.get_json())
        # Create crew member instance
        new_crew_member = create_or_update_crew_member(CrewMember(), body_data)
        # Add new crew member and commit
        db.session.add(new_crew_member)
        db.session.commit()
        return CrewMemberSchema().dump(new_crew_member)
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique_constraint_violoation
            return {"message": err.orig.diag.message_detail}, 409


# Update - /crew_members/id - PUT and PATCH
@crew_members_bp.route("/<int:crew_member_id>", methods=["PUT", "PATCH"])
def update_crew_member(crew_member_id):
    crew_member = get_crew_member_id(crew_member_id)
    if not crew_member:
        return crew_member_not_found_message(crew_member_id)
    body_data = CrewMemberSchema().load(request.get_json(), partial=True)
    updated_crew_member = create_or_update_crew_member(crew_member, body_data)
    db.session.commit()
    return CrewMemberSchema().dump(updated_crew_member)
    

# Delete - /crew_members/id - DELETE
@crew_members_bp.route("<int:crew_members_id>", methods=["DELETE"])
def delete_crew_member(crew_members_id):
    crew_member = get_crew_member_id(crew_members_id)
    if not crew_member:
        return crew_member_not_found_message(crew_members_id)
    db.session.delete(crew_member)
    db.session.commit()
    return {"message": f"crew_member with name: '{crew_member.name}' deleted successfully"}