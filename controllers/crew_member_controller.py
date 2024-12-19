from flask import Blueprint, request
from init import db
from models.crew_member import CrewMember, CrewMemberSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

crew_members_bp = Blueprint("crew_members", __name__, url_prefix="/crew_members")

# Function to get crew_member id


# Function to send crew member not found message


# Function to create or update information


# Read all - /crew_members - GET
@crew_members_bp.route("/", methods=["GET"])
def get_crew_members():
    crew_id = request.args.get("crew_id")
    stmt = db.select(CrewMember).order_by(CrewMember.crew_member_id)
    crew_members_list = db.session.scalars(stmt)
    return CrewMemberSchema(many=True).dump(crew_members_list)


# Read one - /crew_members/id - GET


# Create - /crew_members - POST


# Update - /crew_members/id - PUT and PATCH


# Delete - /crew_members/id - DELETE
