from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from exceptions import InvalidAPIUsageError
from session_factory import db


def build_error_handlers(app):
    @app.errorhandler(SQLAlchemyError)
    def handle_db_exceptions(ex):
        app.logger.error(f"Error: {ex}")
        db.session.rollback()

    @app.errorhandler(InvalidAPIUsageError)
    def handle_invalid_api_usage(ex):
        return jsonify(ex.to_dict()), ex.status_code
