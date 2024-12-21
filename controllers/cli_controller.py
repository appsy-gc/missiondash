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
            datetime="2024-12-25 12:30:00",
            status="Planning"
        ),
        Mission(
            objective="Search and Rescue Operation",
            location="Sector Delta",
            datetime="2024-12-26 14:45:00",
            status="Planning"
        ),
        Mission(
            objective="Routine Perimeter Sweep",
            location="Home base",
            datetime="2024-12-26 14:45:00",
            status="Planning"
        )
    ]
    jets = [
        Jet(
            model="F16A",
            tail_no ="696VFR",
            availability="On Mission",
            capacity=1,
            last_maint="2024-12-01"
        ),
        Jet(
            model="B2Bomber",
            tail_no ="222BOB",
            availability="Serviceable",
            capacity=2,
            last_maint="2024-11-15"
        ),
        Jet(
            model="C17Globemaster",
            tail_no ="001GBM",
            availability="Serviceable",
            capacity=3,
            last_maint="2024-11-30"
        ),
        Jet(
            model="X-Wing",
            tail_no ="000XXX",
            availability="Serviceable",
            capacity=2,
            last_maint="2024-11-30"
        )
    ]
    crews = [
        Crew(
            name="Alpha" # Pilot only
        ),
        Crew(
            name="Bravo" # Pilot and Co-pilot
        ),
        Crew(
            name="Charlie" # Pilot, Co-pilot and Loadmaster
        ),
        Crew(
            name="Delta" # Pilot only
        ),
        Crew(
            name="Echo" # Pilot and Co-pilot
        )
    ]
    db.session.add_all(crews)
    db.session.commit()

    crew_members = [
        CrewMember(
            crew_id=1,
            name="John Smith",
            role="Pilot",
            availability="On Mission"
        ),
        CrewMember(
            crew_id=2,
            name="Alice Johnson",
            role="Co-pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=3,
            name="Robert Brown",
            role="Co-pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=3,
            name="Emily Davis",
            role="Pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=3,
            name="Michael Taylor",
            role="Loadmaster",
            availability="Available"
        ),
        CrewMember(
            crew_id=2,
            name="Sarah Wilson",
            role="Pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=4,
            name="Barry Allen",
            role="Pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=5,
            name="Jessica Black",
            role="Pilot",
            availability="Available"
        ),
        CrewMember(
            crew_id=5,
            name="Jeff Stallion",
            role="Co-pilot",
            availability="Available"
        ),
    ]

    db.session.add_all(missions)
    db.session.add_all(jets)
    db.session.add_all(crew_members)

    assignments = [
        Assignment(
            jet_id=1,
            mission_id=1,
            crew_id=1
        )
    ]
    db.session.add_all(assignments)
    db.session.commit()
    print("Tables seeded")