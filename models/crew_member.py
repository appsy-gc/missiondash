from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp, OneOf

VALID_ROLES = ("Pilot", "Commander", "Flight Engineer", "Navigator", "Weapons Specialist")
VALID_AVAILABILITY = ("Available","On Mission", "On Leave", "Unavailable", "In Training", "Retired")

class CrewMember(db.Model):
    __tablename__ = "crew_members"

    crew_member_id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.Integer, db.ForeignKey("crews.crew_id", ondelete="CASCADE"))
    crew = db.relationship("Crew", back_populates="crew_members")
    name = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String, nullable=False)

class CrewMemberSchema(ma.Schema):
    # Validation for crew member name
    name = fields.String(
        validate=[
        Length(min=6, error="Crew name must have more than 6 characters."),
        Regexp(
            r'^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$',
            error="Each word must start with a capital letter and contain only letters."
            )
        ],
        required=True   
    )
    # Validation for crew member role
    role = fields.String(validate=OneOf(VALID_ROLES), required=True)
    # Validation for crew member availability
    availability = fields.String(validate=OneOf(VALID_AVAILABILITY), required=True)

    crew = fields.Nested("CrewSchema", only=["name"])
     
    class Meta:
        fields = ("crew_member_id", "crew", "name", "role", "availability")
        ordered = True

crew_member_schema = CrewMemberSchema()
crew_members_schema = CrewMemberSchema(many=True)