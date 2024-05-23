from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session

from models.model_base import ModelBase

db = SQLAlchemy(model_class=ModelBase, session_options={"expire_on_commit": False})


@contextmanager
def get_session() -> Session:
    try:
        yield db.session()
    except SQLAlchemyError as err:
        db.session.rollback()
        print(f"Oops! {err}")
    except OperationalError as err:
        db.session.rollback()
        print(f"Oops! {err}")
    else:
        db.session.commit()
