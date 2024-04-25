import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# noinspection PyPackageRequirements
from models.model_base import ModelBase


class Move(ModelBase):
    __tablename__ = 'moves'
    __table_args__ = (
        Index(None, "player_id", "id", "is_winning_play"),  # create multicolumn index
        # {"schema": "main"},  # set table schema
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    roll_id: Mapped[int] = mapped_column(Integer, ForeignKey("rolls.id"), nullable=False)
    game_id: Mapped[int] = mapped_column(String, nullable=False)
    roll_number: Mapped[int] = mapped_column(Integer, nullable=False)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("player.id"), nullable=False)
    is_winning_play: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, index=True)

    def __repr__(self) -> str:
        return f"Move(id={self.id!r}, roll_id={self.roll_id!r}, game_id={self.game_id!r}, \
                    roll_number={self.roll_number!r}, player_id={self.player_id!r}, \
                    is_winning_play={self.is_winning_play!r}, created={self.created!r})"
