from init import db, ma
from marshmallow import fields, validates, ValidationError
from models.mission import Mission
from models.jet import Jet
from models.crew import Crew
from marshmallow.validate import Length, Regexp, OneOf

def validate_id(model, value, field_name):
    # Check if the ID is an integer and not empty
    if not isinstance(value, int):
        raise ValidationError(f"{field_name} must be a valid integer.")
    # Check if the ID exists in the database
    instance = db.session.get(model, value)
    if not instance:
        raise ValidationError(f"{field_name} with ID {value} does not exist.")


class Assignment(db.Model):
    __tablename__ = "assignments"

    assign_id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey("missions.mission_id", ondelete="CASCADE"), nullable=False)
    mission = db.relationship("Mission", back_populates="assignments")
    jet_id = db.Column(db.Integer, db.ForeignKey("jets.jet_id", ondelete="CASCADE"), nullable=False)
    jet = db.relationship("Jet", back_populates="assignments")
    crew_id = db.Column(db.Integer, db.ForeignKey("crews.crew_id", ondelete="CASCADE"), nullable=False)
    crew = db.relationship("Crew", back_populates="assignments")
    

class AssignmentSchema(ma.Schema):

    mission = fields.Nested("MissionSchema", exclude=["mission_id"])
    jet = fields.Nested("JetSchema", exclude=["jet_id"])
    crew = fields.Nested("CrewSchema", exclude=["crew_id"])

    class Meta:
        fields = ("assign_id", "mission_id", "mission", "jet_id", "jet", "crew_id", "crew")
        ordered = True

    @validates("mission_id")
    def validate_mission_id(self, value):
        validate_id(Mission, value, "Mission ID")

    @validates("jet_id")
    def validate_jet_id(self, value):
        validate_id(Jet, value, "Jet ID")
    
    @validates("crew_id")
    def validate_crew_id(self, value):
            validate_id(Crew, value, "Crew ID")

assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)