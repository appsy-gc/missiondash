from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Crew(db.Model):
    __tablename__ = "crews"

    crew_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class CrewSchema(ma.Schema):
    # Validation for crew name
    name = fields.String(
        validate=[
        Length(max=10, error="Crew name must be less than 10 characters."),
        Regexp(
            r'^[A-Z][a-zA-Z]*$',
            error="Name must start with a capital letter and contain only letters."
            )
        ],
        required=True   
    )
     
    class Meta:
        fields = ("crew_id", "name")
        ordered = True

crew_schema = CrewSchema()
crews_schema = CrewSchema(many=True)