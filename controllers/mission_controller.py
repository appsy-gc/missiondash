from flask import Blueprint, request
from init import db
from models.mission import Mission, MissionSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

missions_bp = Blueprint("missions", __name__, url_prefix="/missions")

# Function for getting mission id
def get_mission_by_id(mission_id):
    stmt = db.select(Mission).filter_by(mission_id=mission_id)
    return db.session.scalar(stmt)

# Function for when a mission id cannot be found
def mission_not_found(mission_id):
    return {"message": f"Mission with id: {mission_id} does not exist"}, 404

# Function to create or update information
def create_or_update_mission(mission, body_data):
    for attr in ["objective", "location", "datetime", "status"]:
        setattr(mission, attr, body_data.get(attr, getattr(mission, attr)))
    return mission

# Read all - /missions - GET
@missions_bp.route("/")
def get_missions():
    stmt = db.select(Mission)
    missions_list = db.session.scalars(stmt)
    data = MissionSchema(many=True).dump(missions_list)
    return data

# Read one - /missions/id - GET
@missions_bp.route("/<int:mission_id>")
def get_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    if mission:
        data = MissionSchema().dump(mission)
        return data
    else:
        return mission_not_found(mission_id)

# Create - /missions - POST
@missions_bp.route("/", methods=["POST"])
def create_mission():
    try:
        # Get information from request body
        body_data = MissionSchema().load(request.get_json())
        # Create mission instance
        new_mission = create_or_update_mission(Mission(), body_data)
        # Add new mission and commit
        db.session.add(new_mission)
        db.session.commit()
        return MissionSchema().dump(new_mission), 201   
    except ValidationError as err:
        # Catch and handle validation errors
        return {"message": err.messages}, 400    
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violoation
            # Return specific field that is in violoation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        return {"message": "An unexpected database error occurred."}, 500

# Update - /missions/id - PUT and PATCH
@missions_bp.route("/<int:mission_id>", methods=["PUT", "PATCH"])
def update_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    if not mission:
        return mission_not_found(mission_id)
    body_data = MissionSchema().load(request.get_json(), partial=True)
    updated_mission = create_or_update_mission(mission, body_data)
    db.session.commit()
    return MissionSchema().dump(updated_mission)

# Delete - /missions/id - DELETE
@missions_bp.route("<int:mission_id>", methods=["DELETE"])
def delete_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    if mission:
        db.session.delete(mission)
        db.session.commit()
        return {"message": f"Mission: '{mission.objective}' deleted successfully"}
    else:
        return mission_not_found(mission_id)