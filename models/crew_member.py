from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, Regexp

class CrewMember(db.Model):
    __tablename__ = "crew_members"

    crew_member_id = db.Column(db.Integer, primary_key=True)
    crew_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String, nullable=False)

class CrewMemberSchema(ma.Schema):
    # Validation for crew name
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
     
    class Meta:
        fields = ("crew_member_id", "crew_id", "name", "role", "availability")
        ordered = True

crew_member_schema = CrewMemberSchema()
crew_members_schema = CrewMemberSchema(many=True)