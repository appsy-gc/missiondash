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
@statuses_bp.route("/", methods=["POST"])
def create_status():
    try:
        # Get information from request body
        body_data = StatusSchema().load(request.get_json(), partial=True)
        # Create status instance
        new_status = Status(
            name = body_data.get("name")
        )
        # Add new status and commit
        db.session.add(new_status)
        db.session.commit()
        return StatusSchema().dump(new_status), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                # unique_constraint_violoation
                return {"message": "Status name already exists"}, 409

# Update - /statuses/id - PUT and PATCH


# Delete - /statuses/id - DELETE