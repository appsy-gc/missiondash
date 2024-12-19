from flask import Blueprint, request
from init import db
from models.jet import Jet, JetSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

jets_bp = Blueprint("jets", __name__, url_prefix="/jets")

# Function for getting jet id
def get_jet_by_id(jet_id):
    stmt = db.select(Jet).filter_by(jet_id=jet_id)
    return db.session.scalar(stmt)

# Function for when a mission id cannot be found
def jet_not_found(jet_id):
    return {"message": f"Mission with id: {jet_id} does not exist"}, 404

# Function to create or update information
def create_or_update_jet(jet, body_data):
    for attr in ["model", "tail_no", "availability", "last_maint"]:
        setattr(jet, attr, body_data.get(attr, getattr(jet, attr)))
    return jet

# Read all - /jets - GET
@jets_bp.route("/")
def get_jets():
    stmt = db.select(Jet)
    jets_list = db.session.scalars(stmt)
    return JetSchema(many=True).dump(jets_list)

# Read one - /jets/id - GET
@jets_bp.route("/<int:jet_id>")
def get_jet(jet_id):
    jet = get_jet_by_id(jet_id)
    if jet:
        return JetSchema().dump(jet)
    else:
        return jet_not_found(jet_id)

# Create - /jets - POST
@jets_bp.route("/", methods=["POST"])
def create_jet():
    try:
        # Get information from request body
        body_data = JetSchema().load(request.get_json())
        # Create jet instance
        new_jet = create_or_update_jet(Jet(), body_data)
        # Add new jet and commit
        db.session.add(new_jet)
        db.session.commit()
        return JetSchema().dump(new_jet), 201   
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
            tail_no = body_data.get("tail_no", "unknown")
            return {"message": f"Jet with tail number: '{tail_no}' already exists"}, 409
        return {"message": "An unexpected database error occurred."}, 500

# Update - /jets/id - PUT and PATCH
@jets_bp.route("/<int:jet_id>", methods=["PUT", "PATCH"])
def update_jet(jet_id):
    jet = get_jet_by_id(jet_id)
    if not jet:
        return jet_not_found(jet_id)
    body_data = JetSchema().load(request.get_json(), partial=True)
    updated_jet = create_or_update_jet(jet, body_data)
    db.session.commit()
    return JetSchema().dump(updated_jet)

# Delete - /jets/id - DELETE
@jets_bp.route("<int:jet_id>", methods=["DELETE"])
def delete_jet(jet_id):
    jet = get_jet_by_id(jet_id)
    if not jet:
        return jet_not_found(jet_id)
    db.session.delete(jet)
    db.session.commit()
    return {"message": f"Jet with tail number: '{jet.tail_no}' deleted successfully"}
        