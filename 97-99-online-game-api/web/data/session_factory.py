from contextlib import contextmanager

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session

from web.db import db_folder
from web.models.model_base import ModelBase

__factory = None


def global_init():
    global __factory

    full_file = db_folder.get_db_path('rock_paper_scissors.sqlite')
    conn_str = 'sqlite:///' + full_file
    engine = sa.create_engine(conn_str, echo=False, pool_size=10, )
    ModelBase.metadata.create_all(engine, checkfirst=True, )

    __factory = orm.sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_session() -> Session:
    global __factory

    if __factory is None:
        global_init()

    session = orm.scoped_session(__factory)

    try:
        yield session
    except SQLAlchemyError as err:
        session.rollback()
        print(f"Oops! {err}")
    except OperationalError as err:
        session.rollback()
        print(f"Oops! {err}")
    finally:
        session.commit()
