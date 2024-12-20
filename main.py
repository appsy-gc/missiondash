# Import packages
import os
from flask import Flask
from marshmallow.exceptions import ValidationError

# Import from init.py
from init import db, ma

# Import blueprint from cli_controller
from controllers.cli_controller import Blueprint, db_commands
# Import blueprint from mission_controller
from controllers.mission_controller import Blueprint, missions_bp
# Import blueprint from jet_controller
from controllers.jet_controller import Blueprint, jets_bp
# Import blueprint from crew_controller
from controllers.crew_controller import Blueprint, crews_bp
# Import blueprint from crew_member_controller
from controllers.crew_member_controller import Blueprint, crew_members_bp
# Import blueprint from assignment_controller
from controllers.assignment_controller import Blueprint, assignments_bp

def create_app():
    app = Flask(__name__)

    print("Server started...")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Stop flask from ordering data
    app.json.sort_keys = False

    # Initialise SQLAlchemy
    db.init_app(app)
    # Initialise Marshmallow
    ma.init_app(app)

    # Global error handling by marshmallow
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"message": err.messages}, 400
    
    # General validation handlers for 400 bad request and 404 not found
    @app.errorhandler(400)
    def bad_request(err):
        return {"message": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"message": str(err)}, 404
    
    # Register cli_controller
    app.register_blueprint(db_commands)
    # Register mission_controller
    app.register_blueprint(missions_bp)
    # Register jet_controller
    app.register_blueprint(jets_bp)
    # Register crew_controller
    app.register_blueprint(crews_bp)
    # Register crew_member_controller
    app.register_blueprint(crew_members_bp)
    # Register assignment_controller
    app.register_blueprint(assignments_bp)

    return app