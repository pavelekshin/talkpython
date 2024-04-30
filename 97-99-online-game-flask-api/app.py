from flask import Flask
from config.config import ProductionConfig
from services import game_service, game_decider
from views import home, game_api


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object(ProductionConfig(name="rock_paper_scissors.sqlite"))
    else:
        app.config.from_object(config)
    with app.app_context():
        from data.session_factory import db
        db.init_app(app)
        db.create_all()
        build_views(app)
        build_starter_data()
    return app


def build_views(app: Flask):
    game_api.build_views(app)
    home.build_views(app)


def build_starter_data():
    roll_names = game_decider.all_roll_names()
    game_service.init_rolls(roll_names)

    if not (computer := game_service.find_player("computer")):
        game_service.create_player("computer")


if __name__ == "__main__":
    flaskapp = create_app()
    flaskapp.run(debug=False)
