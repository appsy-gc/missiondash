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
    if crew_member:
        return CrewMemberSchema().dump(crew_member)
    else:
        return crew_member_not_found_message(crew_member_id)


# Create - /crew_members - POST


# Update - /crew_members/id - PUT and PATCH


# Delete - /crew_members/id - DELETE
