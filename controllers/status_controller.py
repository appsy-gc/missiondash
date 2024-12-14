from flask import Blueprint, request
from init import db
from models.status import Status, StatusSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

statuses_bp = Blueprint("statuses", __name__, url_prefix="/statuses")

# Read all - /statuses - GET
@statuses_bp.route("/")
def get_statuses():
    stmt = db.select(Status)
    statuses_list = db.session.scalars(stmt)
    data = StatusSchema(many=True).dump(statuses_list)

    return data

# Read one - /statuses/id - GET


# Create - /statuses - POST


# Update - /statuses/id - PUT and PATCH


# Delete - /statuses/id - DELETE