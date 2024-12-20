from flask import Blueprint
from init import db
from models.mission import Mission
from models.jet import Jet
from models.crew import Crew
from models.crew_member import CrewMember
from models.assignments import Assignment

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
            tail_no ="696VFR",
            availability="Serviceable",
            last_maint="2024-12-01"
        ),
        Jet(
            model="B2Bomber",
            tail_no ="222BOB",
            availability="On Mission",
            last_maint="2024-11-15"
        ),
        Jet(
            model="F22",
            tail_no ="022RAP",
            availability="Serviceable",
            last_maint="2024-10-25"
        ),
        Jet(
            model="XWing",
            tail_no ="999XWG",
            availability="Unserviceable",
            last_maint="2024-12-10"
        ),
        Jet(
            model="Raptor7",
            tail_no ="007RAP",
            availability="Serviceable",
            last_maint="2024-11-30"
        )
    ]
    crews = [
        Crew(
            name="Alpha"
        ),
        Crew(
            name="Beta"
        ),
        Crew(
            name="Charlie"
        ),
        Crew(
            name="Delta"
        ),
        Crew(
            name="Echo"
        )
    ]
    db.session.add_all(crews)
    db.session.commit()

    crew_members = [
        CrewMember(
            crew_id=1,
            name="John Smith",
            role="Pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=1,
            name="Alice Johnson",
            role="Commander",
            availability="On Mission"
        ),
        CrewMember(
            crew_id=2,
            name="Robert Brown",
            role="Flight Engineer",
            availability="In Training"
        ),
        CrewMember(
            crew_id=2,
            name="Emily Davis",
            role="Navigator",
            availability="On Leave"
        ),
        CrewMember(
            crew_id=3,
            name="Michael Taylor",
            role="Weapons Specialist",
            availability="Unavailable"
        ),
        CrewMember(
            crew_id=3,
            name="Sarah Wilson",
            role="Pilot",
            availability="Retired"
        )
    ]

    db.session.add_all(missions)
    db.session.add_all(jets)
    db.session.add_all(crew_members)

    assignments = [
        Assignment(
            crew_id=1,
            jet_id=1,
            mission_id=1
        ),
        Assignment(
            crew_id=2,
            jet_id=3,
            mission_id=2
        ),
        Assignment(
            crew_id=3,
            jet_id=2,
            mission_id=3
        )
    ]
    db.session.add_all(assignments)
    db.session.commit()
    print("Tables seeded")