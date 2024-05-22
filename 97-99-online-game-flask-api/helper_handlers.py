import flask


def build_before_after_request_handlers(app):
    @app.before_request
    def log_request():
        app.logger.info(
            "path: {} | method: {} | body: {}".format(
                flask.request.path,
                flask.request.method,
                flask.request.get_json()
                if flask.request.is_json
                else flask.request.data,
            )
        )

    @app.after_request
    def log_response(response: flask.Response):
        app.logger.info(
            "status: {} | body: {}".format(
                response.status, response.get_data(as_text=True)
            )
        )
        return response
