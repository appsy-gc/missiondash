from flask import Blueprint
from init import db
from models.status import Status

db_commands = Blueprint("db", __name__)

# Create tables
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

# Drop tables
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# Seed tables
@db_commands.cli.command("seed")
def seed_tables():
    statuses = [
        Status(
            name = "Planning"
        ),
        Status(
            name = "Scheduled"
        ),
        Status(
            name = "In Progress"
        ),
        Status(
            name = "Completed - Success"
        ),
        Status(
            name = "Completed - Failure"
        )
    ]

    db.session.add_all(statuses)
    db.session.commit()
    print("Tables seeded")