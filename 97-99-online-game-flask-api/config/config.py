from db.db_folder import get_db_path


class Config:
    """Base config, uses staging database server."""

    __test__ = False
    TESTING = False
    DB_SERVER = "localhost"
    DB_USER = None
    DB_PASSWORD = None
    DB_NAME = None
    ECHO = False
    DEBUG = False
    ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_pre_ping": True,
    }

    @property
    def sqlalchemy_database_uri(self):  # noqa
        raise NotImplementedError("Not implemented")

    @property
    def sqlalchemy_engine_options(self):  # noqa
        return self.ENGINE_OPTIONS

    @property
    def sqlalchemy_echo(self):  # noqa
        return self.ECHO


class ProductionConfig(Config):
    """Uses production database server."""

    pass


class DevelopmentConfig(Config):
    """Uses development database server."""

    TESTING = True
    ECHO = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    def __init__(self, db_name=None):
        if db_name is None:
            raise AttributeError("Database name not provided!")
        self.db_name = db_name
        self.SQLALCHEMY_DATABASE_URI += str(self._db_filename())

    def _db_filename(self):
        return get_db_path(self.db_name)


class TestingConfig(Config):
    """Uses testing server."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ECHO = False
    DEBUG = True
    ENGINE_OPTIONS = {}
