import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, DateTime, Index
from web.models.model_base import ModelBase


class Roll(ModelBase):
    __tablename__ = "rolls"
    __table_args__ = (
        Index(None, "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "created": self.created.isoformat(),
            "name": self.name,
        }

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(id={self.id!r}, name={self.name!r}, created={self.created!r})"
