from flask import Blueprint
from init import db
from models.mission import Mission

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
    missions = [
        Mission(
            objective="Reconnaissance of Sector Alpha",
            location="Sector Alpha",
            datetime="2024-12-14 08:00:00",  # Use YYYY-MM-DD HH:MM:SS format
            status="Scheduled"
        ),
        Mission(
            objective="Airspace Patrol",
            location="Sector Bravo",
            datetime="2024-12-15 12:30:00",
            status="In Progress"
        ),
        Mission(
            objective="Search and Rescue Operation",
            location="Sector Delta",
            datetime="2024-12-16 14:45:00",
            status="Planning"
        )
    ]
    db.session.add_all(missions)
    db.session.commit()
    print("Tables seeded")