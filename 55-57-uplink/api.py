from uplink import Consumer, get, returns, Query, response_handler, error_handler
import logging

api_log = logging.getLogger(__name__)


def raise_for_status(response):
    """Checks whether or not the response was successful."""

    api_log.debug(
        "Request to {}, with headers {}, complite with status {}".format(
            response.request.url, response.request.headers, response.status_code
        )
    )

    api_log.debug(
        "Reponse headers {}, response body {}.".format(
            response.headers, response.content
        )
    )

    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response

    api_log.warn(
        "Error on request {}, response body {}, status code {} ".format(
            response.url, response.content, response.status_code
        )
    )
    raise UnsuccessfulRequest(response.url)


def raise_api_error(e_type, e_instance, e_traceback):
    """Wraps client error with custom API error"""
    api_log.warn(
        "Exception {}, rised {} with traceback {}.".format(
            e_type, e.instance, e_traceback
        )
    )
    api_log.exception(
        "Exception {}, rised {} with traceback {}.".format(
            e_type, e.instance, e_traceback
        )
    )


@returns.json
@response_handler(raise_for_status)
@error_handler(raise_api_error)
class MovieSearch(Consumer):
    def __init__(self, base_url, apikey):
        super(MovieSearch, self).__init__(base_url=base_url)
        # Send the API token as a query parameter with each request.
        self.session.params["apikey"] = apikey

    @get
    def search_movie(self, s: Query, y: Query = None):
        """Returns search result for entered keywoard and year"""

    @get
    def search_movie_title(self, t: Query, y: Query = None):
        """Returns search result for entered Title movie and year"""

    @get
    def search_movie_id(self, i: Query):
        """Returns search result for movie ID"""
