from flask import Blueprint
from init import db
from models.mission import Mission
from models.jet import Jet

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
    jets = [
        Jet(
            model="F16A",
            availability="Serviceable",
            last_maint="2024-12-01"
        ),
        Jet(
            model="B2Bomber",
            availability="On Mission",
            last_maint="2024-11-15"
        ),
        Jet(
            model="F22",
            availability="Serviceable",
            last_maint="2024-10-25"
        ),
        Jet(
            model="XWing",
            availability="Unserviceable",
            last_maint="2024-12-10"
        ),
        Jet(
            model="Raptor7",
            availability="Serviceable",
            last_maint="2024-11-30"
        )
    ]
    db.session.add_all(missions)
    db.session.add_all(jets)
    db.session.commit()
    print("Tables seeded")