from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = ("Planning", "Scheduled", "In Progress", "Completed - Success", "Completed - Failure")

class Status(db.Model):
    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class StatusSchema(ma.Schema):
    # Force status name to be only a valid status
    name = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("status_id", "name")
        ordered = True

status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)