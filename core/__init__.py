from flask import Flask

from structure.school import School

school = School()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    with app.app_context():
        # Imports
        from . import routes
        from . import message_handlers

        return app
