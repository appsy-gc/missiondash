from init import db, ma
from marshmallow import fields, validates, ValidationError, validates_schema
from models.mission import Mission
from models.jet import Jet
from models.crew import Crew
from models.crew_member import CrewMember
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

    @validates_schema
    def validate_unique_combination(self, data, **kwargs):
        mission_id = data.get("mission_id")
        jet_id = data.get("jet_id")
        crew_id = data.get("crew_id")

        # Check if an assignment with the same combination exists
        existing_assignment = db.session.query(Assignment).filter_by(
            mission_id=mission_id,
            jet_id=jet_id,
            crew_id=crew_id
        ).first()

        if existing_assignment:
            raise ValidationError(
                f"Assignment with mission_id={mission_id}, jet_id={jet_id}, and crew_id={crew_id} already exists."
            )
        
    @validates_schema
    def validate_assignment(self, data, **kwargs):
        # Fetch the jet and related crew members
        jet = db.session.get(Jet, data["jet_id"])
        if not jet:
            raise ValidationError("Jet does not exist.", field_name="jet_id")

        crew_members = CrewMember.query.filter_by(crew_id=data["crew_id"]).all()

        # 1. Check if jet capacity matches the number of crew members
        if len(crew_members) != jet.capacity:
            raise ValidationError(
                f"Jet capacity is {jet.capacity}, but {len(crew_members)} crew members are assigned.",
                field_name="jet_id",
            )

        # 2. Check if there is exactly one pilot in the crew
        pilots = [cm for cm in crew_members if cm.role == "Pilot"]
        if len(pilots) == 0:
            raise ValidationError("Every assignment must include one pilot.", field_name="crew_id")
        elif len(pilots) > 1:
            raise ValidationError("Too many pilots in the assignment.", field_name="crew_id")

        # 3. Check if all crew members are available
        unavailable_members = [cm for cm in crew_members if cm.availability not in ["Available", "In Training"]]
        if unavailable_members:
            raise ValidationError(
                f"The following crew members are not available: "
                f"{', '.join(cm.name for cm in unavailable_members)}.",
                field_name="crew_id",
            )

        # 4. Check if the jet is serviceable
        if jet.availability not in ["Serviceable"]:
            raise ValidationError(
                f"The jet is currently {jet.availability.lower()} and cannot be assigned.",
                field_name="jet_id",
            )

assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)