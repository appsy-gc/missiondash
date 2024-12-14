from init import db, ma
from marshmallow import fields

class Mission(db.Model):
    __tablename__ = "missions"

    mission_id = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    status = db.Column(db.String, nullable=False)

class MissionSchema(ma.Schema):
    ordered = True
    class Meta:
        fields = ("mission_id", "objective", "location", "date", "status")

mission_schema = MissionSchema()
missions_schema = MissionSchema(many=True)