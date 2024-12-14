from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_STATUSES = ("Planning", "Scheduled", "In Progress", "Completed - Success", "Completed - Failure")

class Status(db.Model):
    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class StatusSchema(ma.Schema):
    # Force status name to be only a valid status
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("status_id", "name")
        ordered = True

status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)