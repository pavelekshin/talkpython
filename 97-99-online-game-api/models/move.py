import datetime

from data.session_factory import db
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.player import Player
from models.roll import Roll


class Move(db.Model):
    __table_args__ = (
        Index(None, "player_id", "id", "is_winning_play"),  # create multicolumn index
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    roll_id: Mapped[int] = mapped_column(Integer, ForeignKey("roll.id"), nullable=False)
    game_id: Mapped[int] = mapped_column(String, nullable=False)
    roll_number: Mapped[int] = mapped_column(Integer, nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), nullable=False)
    is_winning_play: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, index=True)

    def to_json(self, roll: Roll, player: Player):
        if self.roll_id != roll.id:
            raise Exception("Mismatched roll values")
        if self.player_id != player.id:
            raise Exception("Mismatched player values")

        return {
            "id": self.id,
            "created": self.created.isoformat(),
            "roll_id": self.roll_id,
            "roll": roll.name,
            "player_id": self.player_id,
            "player": player.name,
            "roll_number": self.roll_number,
            "is_winning_play": self.is_winning_play,
        }

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(id={self.id!r}, roll_id={self.roll_id!r}, game_id={self.game_id!r}, \
                    roll_number={self.roll_number!r}, player_id={self.player_id!r}, \
                    is_winning_play={self.is_winning_play!r}, created={self.created!r})"
