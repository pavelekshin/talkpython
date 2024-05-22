from flask import Flask

from config.config import DevelopmentConfig
from error_handlers import build_error_handlers
from helper_handlers import build_before_after_request_handlers
from services import game_decider, game_service
from views import game_api, home


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object(DevelopmentConfig(db_name="rock_paper_scissors.sqlite"))
    else:
        app.config.from_object(config)
    with app.app_context():
        from session_factory import db

        db.init_app(app)
        db.create_all()
        build_views(app)
        build_starter_data()
    return app


def build_views(app: Flask):
    game_api.build_views(app)
    home.build_views(app)
    build_error_handlers(app)
    build_before_after_request_handlers(app)


def build_starter_data():
    roll_names = game_decider.all_roll_names()
    game_service.init_rolls(roll_names)

    if not game_service.find_player("computer"):
        game_service.create_player("computer")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
