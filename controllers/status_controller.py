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
@statuses_bp.route("/<int:status_id>")
def get_status(status_id):
    stmt = db.select(Status).filter_by(status_id=status_id)
    status = db.session.scalar(stmt)

    if status:
        data = StatusSchema().dump(status)
        return data
    else:
        return {"message": f"Status with id: {status_id} does not exist"}, 404

# Create - /statuses - POST


# Update - /statuses/id - PUT and PATCH


# Delete - /statuses/id - DELETE