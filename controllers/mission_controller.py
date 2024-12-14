from flask import Blueprint, request
from init import db
from models.mission import Mission, MissionSchema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from marshmallow.exceptions import ValidationError

missions_bp = Blueprint("missions", __name__, url_prefix="/missions")

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
    stmt = db.select(Mission).filter_by(mission_id=mission_id)
    mission = db.session.scalar(stmt)

    if mission:
        data = MissionSchema().dump(mission)
        return data
    else:
        return {"message": f"Mission with id: {mission_id} does not exist"}, 404

# Create - /missions - POST
@missions_bp.route("/", methods=["POST"])
def create_mission():
    try:
        # Get information from request body
        body_data = MissionSchema().load(request.get_json(), partial=True)

        # Create mission instance
        new_mission = Mission(
            objective = body_data.get("objective"),
            location = body_data.get("location"),
            datetime = body_data.get("datetime"),
            status = body_data.get("status")
        )

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

# Update - /missions/id - PUT and PATCH


# Delete - /missions/id - DELETE