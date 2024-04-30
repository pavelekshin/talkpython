from db.db_folder import get_db_path


class Config(object):
    """Base config, uses staging database server."""
    __test__ = False
    TESTING = False
    DB_SERVER = "localhost"
    ECHO = False
    DEBUG = False

    def __init__(self, name="rock_paper_scissor.sqlite"):
        if name:
            self._name = name

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.DB_SERVER == "localhost":
            return f"sqlite:///{get_db_path(self._name)}"
        else:
            raise NotImplementedError("Not implemented")

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self):
        return {
            "pool_size": 10,
            "pool_pre_ping": True,
        }

    @property
    def SQLALCHEMY_ECHO(self):
        return self.ECHO

    def _db_filename(self):
        return get_db_path(self._name)


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = "localhost"


class DevelopmentConfig(Config):
    """Uses development database server."""
    DB_SERVER = "localhost"
    TESTING = True
    ECHO = True
    DEBUG = True


class TestingConfig(Config):
    """Uses testing server."""
    DB_SERVER = "localhost"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ECHO = False
    DEBUG = True
