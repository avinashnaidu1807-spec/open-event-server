import json
from typing import Union

from flask import make_response
from flask_rest_jsonapi import JsonApiException
from flask_rest_jsonapi.errors import jsonapi_errors


class ErrorResponse(JsonApiException):
    """
    Parent ErrorResponse class for handling json-api compliant errors.
    Inspired by the JsonApiException class of `flask-rest-jsonapi` itself
    """

    headers = {'Content-Type': 'application/vnd.api+json'}

    def __init__(self, source: Union[dict, str], detail=None, title=None, status=None):
        """Initialize a jsonapi ErrorResponse Object

        :param dict source: the source of the error
        :param str detail: the detail of the error
        """

        if isinstance(source, str) and detail is None:
            # We have been passed a single argument, and hence source is unknown
            # so we'll represent source as detail
            super().__init__(None, source)
        else:
            super().__init__(source, detail, title, status)

    def respond(self):
        """
        :return: a jsonapi compliant response object
        """
        dict_ = self.to_dict()
        return make_response(
            json.dumps(jsonapi_errors([dict_])), self.status, self.headers
        )


class ForbiddenError(ErrorResponse):
    """
    Represents a 403 Forbidden error response returned when access is denied.
    """

    title = 'Access Forbidden'
    status = 403


class NotFoundError(ErrorResponse):
    """
    Represents a 404 Not Found error response when the requested resource is not available.
    """

    title = 'Not Found'
    status = 404


class ServerError(ErrorResponse):
    status = 500
    title = 'Internal Server Error'


class UnprocessableEntityError(ErrorResponse):
    """
    Represents a 422 Unprocessable Entity error when the request data is invalid or cannot be processed.
    """

    status = 422
    title = 'Unprocessable Entity'


class BadRequestError(ErrorResponse):
    """
    Represents a 400 Bad Request error when the client sends an invalid request.
    """

    status = 400
    title = 'Bad Request'


class ConflictError(ErrorResponse):
    """
    Represents a 409 Conflict error when a request conflicts with the current state of the resource.
    """

    title = "Conflict"
    status = 409


class MethodNotAllowed(ErrorResponse):
    """
    Represents a 405 Method Not Allowed error when the requested HTTP method is not supported.
    """

    title = "Method Not Allowed"
    status = 405
