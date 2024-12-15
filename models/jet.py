from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_AVAILABILITY = ("Serviceable", "Unserviceable", "On Mission")

class Jet(db.Model):
    __tablename__ = "jets"

    jet_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    tail_no = db.Column(db.String, nullable=False, unique=True)
    availability = db.Column(db.String, nullable=False)
    last_maint = db.Column(db.Date, nullable=False)

class JetSchema(ma.Schema):
    # Force availability name to be only a valid availabiliity
    availability = fields.String(validate=OneOf(VALID_AVAILABILITY))
    # Validation for model, availability and last_maint
    model = fields.String(
        validate=And(
                Length(min=3, max=10, error="Name must be at least three characters long"),
                Regexp(r'^[a-zA-Z0-9!@#$%^&*(),.?":{}|<>_-]+$', error="Only letters, numbers, and special characters are permitted. Spaces are not allowed.")
            ),
        required=True
    )
    tail_no = fields.String(
        validate=And(
                Length(equal=6, error="Tail number must be exactly 6 characters long."),
                Regexp(
                    r'^[0-9]{3}[A-Z]{3}$',
                    error="Tail number must start with three digits followed by three uppercase letters (e.g., '666XXX')."
                )
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