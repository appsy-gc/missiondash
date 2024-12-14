from init import db, ma
from marshmallow import fields, pre_load
from marshmallow.validate import OneOf

VALID_STATUSES = ("Planning", "Scheduled", "In Progress", "Completed - Success", "Completed - Failure")

class Mission(db.Model):
    __tablename__ = "missions"

    mission_id = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=True) 
    status = db.Column(db.String, nullable=False)

class MissionSchema(ma.Schema):
    # Force status name to be only a valid status
    status = fields.String(validate=OneOf(VALID_STATUSES))

    datetime = fields.DateTime(allow_none=True)

    # Custom pre-load processing method in Marshmallow to convert empty strings into None before validation occurs.
    @pre_load
    def process_empty_datetime(self, data, **kwargs):
        """
        Convert empty string datetime to None before validation.
        """
        if "datetime" in data and data["datetime"] == "":
            data["datetime"] = None
        return data
     
    class Meta:
        fields = ("mission_id", "objective", "location", "datetime", "status")
        ordered = True

mission_schema = MissionSchema()
missions_schema = MissionSchema(many=True)