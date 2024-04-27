from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

from db import db_folder
from models.model_base import ModelBase

db = SQLAlchemy(
    model_class=ModelBase,
    session_options={"expire_on_commit": False}
)


def db_filename(name):
    return db_folder.get_db_path(name)


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