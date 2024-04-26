import os

import flask
from services import game_service, game_decider
from data.session_factory import db_filename, db
from views import game_api, home

app = flask.Flask(__name__)


def init_db():
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") \
                                            or "sqlite:///" + db_filename(name="rock_paper_scissors.sqlite")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = \
        {
            "pool_size": 10,
            "pool_pre_ping": True,
        }
    app.config["SQLALCHEMY_ECHO"] = False
    db.init_app(app)


def build_views():
    game_api.build_views(app)
    home.build_views(app)


def build_starter_data():
    roll_names = game_decider.all_roll_names()
    game_service.init_rolls(roll_names)

    computer = game_service.find_player("computer")
    if not computer:
        game_service.create_player("computer")


if __name__ == "__main__":
    with app.app_context():
        init_db()
        db.create_all()
        build_starter_data()
        build_views()
    app.run(debug=True)
