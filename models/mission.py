from init import db, ma
from marshmallow import fields

class Mission(db.Model):
    __tablename__ = "missions"

    mission_id = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=True) # Must be a datetime format DD-MM-YYYY HH:MM:SS
    status = db.Column(db.String, nullable=False)

class MissionSchema(ma.Schema):
    # Set format for datetime
    datetime = fields.DateTime(format="%d-%m-%Y %H:%M:%S")
    
    class Meta:
        fields = ("mission_id", "objective", "location", "datetime", "status")
        ordered = True

mission_schema = MissionSchema()
missions_schema = MissionSchema(many=True)