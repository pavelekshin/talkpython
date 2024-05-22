import random
import uuid

import flask
from flask import Flask, jsonify, request

from exceptions import InvalidAPIUsageError
from schema.schema import CREATE_USER, PLAY_ROUND
from schema.validator import validate
from services import game_service
from services.game import GameRound


def build_views(app: Flask):  # noqa

    @app.route("/api/game/users/<string:user>", methods=["GET"])
    def find_user(user: str):
        player = game_service.find_player(user)
        if not player:
            raise InvalidAPIUsageError("User was not found!", status_code=404)
        return jsonify(player.to_json())

    @app.route("/api/game/users", methods=["PUT"])
    @validate(CREATE_USER)
    def create_user():
        username = flask.request.json.get("user").strip()
        player = game_service.create_player(username)

        return jsonify(player.to_json())

    @app.route("/api/game/games", methods=["GET"])
    def create_game():
        return jsonify({"game_id": str(uuid.uuid4())})

    @app.route("/api/game/rolls", methods=["GET"])
    def all_rolls():
        rolls = [r.name for r in game_service.all_rolls()]
        return jsonify(rolls)

    @app.route("/api/game/<string:game_id>/status", methods=["GET"])
    def game_status(game_id: str):
        is_over = game_service.is_game_over(game_id)
        history = game_service.get_game_history(game_id)

        if not history:
            raise InvalidAPIUsageError(
                f"History for game_id: {game_id} was not found!", status_code=404
            )

        roll_lookup = {r.id: r for r in game_service.all_rolls()}
        player_lookup = {p.id: p for p in game_service.all_players()}

        player1 = game_service.find_player_by_id(history[0].player_id)
        player2 = game_service.find_player_by_id(history[1].player_id)

        wins_p1 = game_service.count_round_wins(player1.id, game_id)
        wins_p2 = game_service.count_round_wins(player2.id, game_id)

        data = {
            "is_over": is_over,
            "moves": [
                h.to_json(roll_lookup[h.roll_id], player_lookup[h.player_id])
                for h in history
            ],
            "player1": player1.to_json(),
            "player2": player2.to_json(),
            "winner": player1.to_json() if wins_p1 >= wins_p2 else player2.to_json(),
        }

        return jsonify(data)

    @app.route("/api/game/top_scores", methods=["GET"])
    def top_scores():
        players = game_service.all_players()
        wins = [
            {"player": p.to_json(), "score": game_service.get_win_count(p)}
            for p in players
        ]

        wins.sort(key=lambda wn: -wn.get("score"))
        return jsonify(wins[:10])

    @app.route("/api/game/play_round", methods=["POST"])
    @validate(PLAY_ROUND)
    def play_round():
        try:
            db_roll, db_user, game_id = game_service.validate_round_request(request)
        except ValueError as ex:
            raise InvalidAPIUsageError(
                "Invalid request: {}".format(ex), status_code=400
            ) from ex

        computer_player = game_service.find_player("computer")
        computer_roll = random.choice(game_service.all_rolls())

        game = GameRound(game_id, db_user, computer_player, db_roll, computer_roll)
        game.play()

        return jsonify(
            {
                "roll": db_roll.to_json(),
                "computer_roll": computer_roll.to_json(),
                "player": db_user.to_json(),
                "opponent": computer_player.to_json(),
                "round_outcome": str(game.decision_p1_to_p2),
                "is_final_round": game.is_over,
                "round_number": game.round,
            }
        )
