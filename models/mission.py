from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_STATUSES = ("Planning", "Scheduled", "In Progress", "Completed - Success")

# Define reusable schema field
class ValidatedString(fields.String):
    def __init__(self, **kwargs):
        super().__init__(
            required=True,
            validate=And(
                Length(min=3, error="Name must be at least three characters long"),
                Regexp(r'^[a-zA-Z0-9 ]+$', error="Only letters, numbers, and spaces are permitted")
            ),
            **kwargs
        )

class Mission(db.Model):
    __tablename__ = "missions"

    mission_id = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    assignments = db.relationship("Assignment", back_populates="mission", cascade="all, delete-orphan")

class MissionSchema(ma.Schema):
    # Force status name to be only a valid status
    status = fields.String(validate=OneOf(VALID_STATUSES))
    # Validation for objective, location and datetime
    objective = ValidatedString()
    location = ValidatedString()
    datetime = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
     
    class Meta:
        fields = ("mission_id", "objective", "location", "datetime", "status")
        ordered = True

mission_schema = MissionSchema()
missions_schema = MissionSchema(many=True)