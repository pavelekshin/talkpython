from collections import defaultdict
from typing import List, Optional

from requests import Request
from sqlalchemy import func, select

from models.move import Move
from models.player import Player
from models.roll import Roll
from services import game_decider
from session_factory import get_session


def get_game_history(game_id: str) -> List[Move]:
    """
    Get game history by game_id
    :param game_id
    """
    with get_session() as session:
        history = (
            session.execute(
                select(Move).filter(Move.game_id == game_id).order_by(Move.roll_number)
            )
            .scalars()
            .all()
        )
    return history


def is_game_over(game_id: str) -> bool:
    """
    Check if game_id have win flag
    :param game_id
    """
    history = get_game_history(game_id)
    return any([h.is_winning_play for h in history])


def get_win_count(player: Player) -> int:
    """
    Return win count for player
    :param player
    """
    with get_session() as session:
        wins = session.execute(
            select(func.count())
            .select_from(Move)
            .filter(Move.player_id == player.id)
            .filter(Move.is_winning_play)
        ).scalar()
    return wins


def find_player(name: str) -> Player:
    """
    Find player by their name and return their object
    :param name - name of flayer
    """
    with get_session() as session:
        player = (
            session.execute(select(Player).filter(Player.name == name))
            .scalars()
            .first()
        )
    return player


def create_player(name: str) -> Player:
    """
    Create player object
    """
    player = find_player(name)
    if player:
        raise ValueError("Player already exists")

    player = Player()
    player.name = name

    with get_session() as session, session.begin():
        session.add(player)
    return player


def all_players() -> List[Player]:
    """
    Get list of players
    """
    with get_session() as session:
        players = session.execute(select(Player)).scalars().all()
    return players


def record_roll(
    player: Player,
    roll: Roll,
    game_id: str,
    is_winning_play: bool,
    roll_num: int,
):
    """
    Record roll into DB table
    :param player
    :param roll
    :param game_id
    :param is_winning_play
    :param roll_num
    """
    move = Move()
    move.player_id = player.id
    move.roll_id = roll.id
    move.game_id = game_id
    move.is_winning_play = is_winning_play
    move.roll_number = roll_num

    with get_session() as session, session.begin():
        session.add(move)


def all_rolls() -> List[Roll]:
    """
    Get all rolls
    """
    with get_session() as session:
        rolls = session.execute(select(Roll)).scalars().all()
    return rolls


def init_rolls(rolls: List[str]):
    """
    Init rolls
    :param rolls - list of rolls name
    """
    with get_session() as session:
        roll_count = session.execute(select(func.count()).select_from(Roll)).scalar()

    if roll_count:
        return

    for roll_name in rolls:
        create_roll(roll_name)


def find_roll(name: str) -> Optional[Roll]:
    """
    Find roll by their name
    :param name - roll name
    """
    with get_session() as session:
        roll = session.execute(select(Roll).filter(Roll.name == name)).scalars().first()
    return roll


def create_roll(name: str) -> Roll:
    """
    Save roll in DB table
    :param name - roll name
    """
    roll = Roll()
    roll.name = name
    with get_session() as session, session.begin():
        session.add(roll)
    return roll


def find_roll_by_id(roll_id: int) -> Roll:
    """
    Find roll by roll_id and return found object
    :param roll_id - roll_id
    """
    with get_session() as session:
        roll = (
            session.execute(select(Roll).filter(Roll.id == roll_id)).scalars().first()
        )
    return roll


def find_player_by_id(player_id: int) -> Player:
    """
    Find player by player_id and return found object
    :param player_id - player_id
    """
    with get_session() as session:
        player = (
            session.execute(select(Player).filter(Player.id == player_id))
            .scalars()
            .first()
        )
    return player


def count_round_wins(player_id: int, game_id: str) -> int:
    """
    Check round score and return wins count
    :param player_id - player_id
    :param game_id - game_id
    """
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
        if outcome == game_decider.Decision.win:
            wins += 1

    return wins


def validate_round_request(request: Request):
    game_id = request.json.get("game_id")
    user = request.json.get("user")
    roll = request.json.get("roll")

    if not (db_user := find_player(user)):
        raise ValueError("No user with name {}".format(user))
    if not (db_roll := find_roll(roll)):
        raise ValueError("No roll with name {}".format(roll))
    if is_game_over(game_id):
        raise ValueError("This game is already over.")

    return db_roll, db_user, game_id
