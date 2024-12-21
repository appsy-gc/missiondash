# Mission Management System

## Purpose
The Mission Management System is a Flask-based web application designed to efficiently manage military or aviation-related missions. It handles the coordination of missions, jets, crews, and assignments while ensuring data validation and consistency. This app supports CRUD (Create, Read, Update, Delete) operations for all entities and provides robust validation to maintain data integrity.

---

## Entities and Their Relationships

### Entities
1. **Mission**
   - Represents a task or operation.
   - Attributes: `mission_id`, `objective`, `location`, `datetime`, `status`.

2. **Jet**
   - Represents a specific aircraft.
   - Attributes: `jet_id`, `model`, `tail_no`, `availability`, `capacity`, `last_maint`.

3. **Crew**
   - Represents a group of personnel.
   - Attributes: `crew_id`, `name`, `crew_members`.

4. **CrewMember**
   - Represents an individual team member.
   - Attributes: `crew_member_id`, `crew_id`, `name`, `role`, `availability`.

5. **Assignment**
   - Links missions, jets, and crews.
   - Attributes: `assign_id`, `mission_id`, `jet_id`, `crew_id`.

### Relationships
- **Mission ↔ Assignment**: A mission can have multiple assignments.
- **Jet ↔ Assignment**: A jet can be used in multiple assignments.
- **Crew ↔ Assignment**: A crew can participate in multiple assignments.
- **Crew ↔ CrewMember**: A crew has multiple members.

---

## Installation Instructions

### Step 1: Install Required Software
1. Download and install [Python](https://www.python.org/downloads/).
2. Download and install [Visual Studio Code (VS Code)](https://code.visualstudio.com/).

### Step 2: Set Up the Environment

#### 1. Install `pip`
`pip` is usually included with Python. Verify installation by running:
```bash
pip --version
```

#### 2. Install Virtual Environment
Create and activate a virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Flask and Other Dependencies
Create a `requirements.txt` file and add the following:
```
flask
flask_sqlalchemy
flask_marshmallow
psycopg2
```
Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Set Up the Database

#### 1. Environment Variables
Create a `.flaskenv` file:
```
FLASK_APP=main
FLASK_DEBUG=1
FLASK_RUN_PORT=8080
DATABASE_URI=your-database-uri
```

#### 2. Run Database Commands
Initialize the database:
```bash
flask db create
flask db seed
```

### Step 4: Run the Application
Start the server:
```bash
flask run
```

---

## How Entities Function

### 1. Mission
Handles mission-related operations like creating, updating, and deleting missions.

#### Code Snippet for Creating a Mission
```python
@missions_bp.route("/", methods=["POST"])
def create_mission():
    body_data = MissionSchema().load(request.get_json())
    new_mission = Mission(**body_data)
    db.session.add(new_mission)
    db.session.commit()
    return MissionSchema().dump(new_mission), 201
```

#### Validation
- Objective and location must be at least 3 characters.
- Status must be one of `Planning`, `Scheduled`, `In Progress`, `Completed - Success`.

### 2. Jet
Manages details about aircraft used in missions.

#### Code Snippet for Fetching Jets
```python
@jets_bp.route("/", methods=["GET"])
def get_jets():
    jets = Jet.query.all()
    return jets_schema.dump(jets)
```

#### Validation
- Tail number must match the format `123ABC`.
- Availability must be one of `Serviceable`, `Unserviceable`, `On Mission`.

### 3. Crew
Represents teams available for assignments.

#### Code Snippet for Updating a Crew
```python
@crews_bp.route("/<int:crew_id>", methods=["PUT"])
def update_crew(crew_id):
    crew = Crew.query.get_or_404(crew_id)
    body_data = request.get_json()
    crew.name = body_data.get("name", crew.name)
    db.session.commit()
    return crew_schema.dump(crew)
```

#### Validation
- Crew names must start with a capital letter and be less than 10 characters.

### 4. CrewMember
Manages individual crew member data.

#### Code Snippet for Validating a CrewMember
```python
@validates("crew_id")
def validate_crew_id(self, value):
    if not Crew.query.get(value):
        raise ValidationError("Crew with this ID does not exist.")
```

#### Validation
- Role must be one of `Pilot`, `Co-Pilot`, `Loadmaster`.
- Name must have a first and last name with each starting with a capital letter.

### 5. Assignment
Links missions, jets, and crews.

#### Code Snippet for Deleting an Assignment
```python
@assignments_bp.route("/<int:assign_id>", methods=["DELETE"])
def delete_assignment(assign_id):
    assignment = Assignment.query.get_or_404(assign_id)
    db.session.delete(assignment)
    db.session.commit()
    return {"message": "Assignment deleted successfully."}
```

#### Validation
- Jet capacity must match the crew size.
- Each assignment must include one pilot.
- Jet must be serviceable.
- Mission status must be `Planning`.

---

## Notes
- Always ensure the `.flaskenv` file is properly configured.
- For database operations, use the provided CLI commands in `cli_controller.py`.
- Refer to individual controller files for specific endpoints and operations.

Enjoy building and managing missions!

