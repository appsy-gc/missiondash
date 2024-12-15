from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_AVAILABILITY = ("Serviceable", "Unserviceable", "On Mission")

def string_validator(min_length=3, max_length=10, regex=None, error_message=None):
    return And(
        Length(min=min_length, max=max_length, error=f"Value must be between min: {min_length} and max: {max_length} characters."),
        Regexp(regex, error=error_message or "Invalid format.")
    )

class Jet(db.Model):
    __tablename__ = "jets"

    jet_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    tail_no = db.Column(db.String, nullable=False, unique=True)
    availability = db.Column(db.String, nullable=False)
    last_maint = db.Column(db.Date, nullable=False)

class JetSchema(ma.Schema):
    # Force availability name to be only a valid availabiliity
    availability = fields.String(validate=OneOf(VALID_AVAILABILITY), required=True)
    # Validation for model, availability and last_maint
    model = fields.String(
        validate=string_validator(
            regex=r'^[a-zA-Z0-9!@#$%^&*(),.?":{}|<>_-]+$',
            error_message="Only letters, numbers, and special characters are permitted. Spaces are not allowed."
        ),
        required=True
    )
    tail_no = fields.String(
        validate=string_validator(
            regex=r'^[0-9]{3}[A-Z]{3}$',
            error_message="Tail number must start with three digits followed by three uppercase letters (e.g., '666XXX').",
            min_length=6,
            max_length=6
        ),
        required=True
    )
    # Validate last_maint format
    last_maint = fields.Date(format="%Y-%m-%d", required=True)
     
    class Meta:
        fields = ("jet_id", "model", "tail_no", "availability", "last_maint")
        ordered = True

jet_schema = JetSchema()
jets_schema = JetSchema(many=True)