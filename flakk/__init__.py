from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import DevConfig

db = SQLAlchemy()

def create_app(config_class=DevConfig):
    """Factory pour créer l'application Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes.questionnaire_routes import bp_questionnaire
    from .routes.question_routes import bp_question
    from .routes.quiz_route import bp_quiz_page

    app.register_blueprint(bp_questionnaire, url_prefix='/api')
    app.register_blueprint(bp_question, url_prefix='/api')
    app.register_blueprint(bp_quiz_page)

    from .commands import syncdb
    app.cli.add_command(syncdb)

    return app