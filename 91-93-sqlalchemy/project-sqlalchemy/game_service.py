from typing import List, Optional

from sqlalchemy import func, select, delete
from models.move import Move
from models.player import Player
from models.roll import Roll
from data import session_factory


def get_game_history(game_id: str) -> List[Move]:
    session = session_factory.get_session()
    with session as session:
        moves = session.execute(
            select(Player.name.label("name"), Move.player_id, Move.roll_number, Roll.name.label("roll"),
                   Move.is_winning_play,
                   Move.game_id).join_from(Move, Player).join_from(Move, Roll) \
                .where(Move.game_id == game_id)).all()
    return moves


def get_win_count(player: Player) -> int:
    session = session_factory.get_session()
    with session as session:
        wins = session.scalars(select(func.count()) \
                               .select_from(Move) \
                               .filter(Move.player_id == player.id) \
                               .filter(Move.is_winning_play)).one()
    return wins


def find_or_create_player(name: str) -> Player:
    session = session_factory.get_session()
    with session as session:
        player = session.scalars(
            select(Player).
            filter(Player.name == name)
        ).first()

    if player:
        return player

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


def record_roll(player, roll: 'Roll', game_id: str, is_winning_play: bool, roll_num: int):
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


def find_roll(name: str) -> Optional[Roll]:
    session = session_factory.get_session()
    with session as session:
        roll = session.scalars(
            select(Roll).
            filter(Roll.name == name)
        ).first()
    return roll


def create_roll(name: str) -> Roll:
    session = session_factory.get_session()
    roll = Roll()
    roll.name = name
    with session as session, session.begin():
        session.add(roll)
        roll = session.scalars(
            select(Roll).
            filter(Roll.id == roll.id)
        ).first()
    return roll


def delete_game_history(game_id: str) -> int:
    session = session_factory.get_session()
    with session as session, session.begin():
        res = session.execute(delete(Move).where(Move.game_id != game_id))
    return int(res.rowcount)
