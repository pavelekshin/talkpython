import functools

from flask import jsonify, request, make_response
import jsonschema


def validate(req_schema):
    """
    Validate ingress request
    :param req_schema — json schema
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                jsonschema.validate(
                    instance=request.json, schema=req_schema
                )
            except jsonschema.ValidationError as ex:
                resp = make_response(
                    jsonify({'status': 'Error', 'description': ex.message})
                )
                resp.status_code = 400
                return resp

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
