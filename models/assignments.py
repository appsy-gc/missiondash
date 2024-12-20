from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, Regexp, OneOf

class Assignment(db.Model):
    __tablename__ = "assignments"

    assign_id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey("missions.mission_id", ondelete="CASCADE"))
    mission = db.relationship("Mission", back_populates="assignments")
    jet_id = db.Column(db.Integer, db.ForeignKey("jets.jet_id", ondelete="CASCADE"))
    jet = db.relationship("Jet", back_populates="assignments")
    crew_id = db.Column(db.Integer, db.ForeignKey("crews.crew_id", ondelete="CASCADE"))
    crew = db.relationship("Crew", back_populates="assignments")
    

class AssignmentSchema(ma.Schema):

    mission = fields.Nested("MissionSchema", exclude=["mission_id"])
    jet = fields.Nested("JetSchema", exclude=["jet_id"])
    crew = fields.Nested("CrewSchema", exclude=["crew_id"])

    class Meta:
        fields = ("assign_id", "mission_id", "mission", "jet_id", "jet", "crew_id", "crew")
        ordered = True

assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)