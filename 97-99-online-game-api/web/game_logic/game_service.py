from collections import defaultdict
from typing import List, Optional

from sqlalchemy import select, func

from web.data import session_factory
from web.game_logic import game_decider
from web.game_logic.game_decider import Decision
from web.models.move import Move
from web.models.player import Player
from web.models.roll import Roll


# def get_game_history(game_id: str) -> List[Move]:
#     session = session_factory.get_session()
#     with session as session:
#         moves = session.execute(
#             select(Player.name.label("name"), Move.player_id, Move.roll_number, Roll.name.label("roll"),
#                    Move.is_winning_play,
#                    Move.game_id).join_from(Move, Player).join_from(Move, Roll)
#             .filter(Move.game_id == game_id)).all()
#         print(moves)
#     return moves


def get_game_history(game_id: str) -> List[Move]:
    session = session_factory.get_session()
    with session as session:
        history = session.scalars(select(Move)
                                  .filter(Move.game_id == game_id)
                                  .order_by(Move.roll_number)
                                  ).all()
    return history


def is_game_over(game_id: str) -> bool:
    history = get_game_history(game_id)
    return any([h.is_winning_play for h in history])


def get_win_count(player: Player) -> int:
    session = session_factory.get_session()
    with session as session:
        wins = session.scalars(select(func.count())
                               .select_from(Move)
                               .filter(Move.player_id == player.id)
                               .filter(Move.is_winning_play)).one()
    return wins


def find_player(name: str) -> Player:
    session = session_factory.get_session()
    with session as session:
        player = session.scalars(
            select(Player).
            filter(Player.name == name)
        ).first()
    return player


def create_player(name: str) -> Player:
    player = find_player(name)
    if player:
        raise ValueError("Player already exists")

    player = Player()
    player.name = name

    session = session_factory.get_session()
    with session as session, session.begin():
        session.add(player)
        player = session.scalars(
            select(Player).
            filter(Player.name == name)
        ).one()

    return player


def all_players() -> List[Player]:
    session = session_factory.get_session()
    with session as session:
        players = session.scalars(select(Player)).all()
    return players


def record_roll(player, roll: Roll, game_id: str, is_winning_play: bool, roll_num: int):
    move = Move()
    move.player_id = player.id
    move.roll_id = roll.id
    move.game_id = game_id
    move.is_winning_play = is_winning_play
    move.roll_number = roll_num
    session = session_factory.get_session()
    with session as session, session.begin():
        session.add(move)


def all_rolls() -> List[Roll]:
    session = session_factory.get_session()
    with session as session:
        rolls = session.scalars(select(Roll)).all()
    return rolls


def init_rolls(rolls: List[str]):
    session = session_factory.get_session()
    with session as session:
        roll_count = session.query(Roll).count()

    if roll_count:
        return

    for roll_name in rolls:
        create_roll(roll_name)


def find_roll(name: str) -> Optional[Roll]:
    session = session_factory.get_session()
    with session as session:
        roll = session.scalars(
            select(Roll).
            filter(Roll.name == name)
        ).first()
    return roll


def create_roll(name: str) -> Roll:
    roll = Roll()
    roll.name = name
    session = session_factory.get_session()
    with session as session, session.begin():
        session.add(roll)
        roll = session.scalars(
            select(Roll).
            filter(Roll.id == roll.id)
        ).first()
    return roll


def find_roll_by_id(roll_id: int) -> Roll:
    session = session_factory.get_session()
    with session as session:
        roll = session.scalars(select(Roll).filter(Roll.id == roll_id)).first()
    return roll


def find_player_by_id(player_id: int) -> Player:
    session = session_factory.get_session()
    with session as session:
        player = session.scalars(select(Player).filter(Player.id == player_id)).first()
    return player


def count_round_wins(player_id: int, game_id: str) -> int:
    history = get_game_history(game_id)
    wins = 0
    grouped_moves = defaultdict(list)

    for h in history:
        grouped_moves[h.roll_number].append(h)

    for rnd_num, moves in grouped_moves.items():
        player_move = [m for m in moves if m.player_id == player_id][0]
        opponent_move = [m for m in moves if m.player_id != player_id][0]

        player_roll = find_roll_by_id(player_move.roll_id)
        opponent_roll = find_roll_by_id(opponent_move.roll_id)

        outcome = game_decider.decide(player_roll, opponent_roll)
        if outcome == Decision.win:
            wins += 1

    return wins
