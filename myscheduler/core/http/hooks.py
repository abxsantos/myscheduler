"""
Hooks module for the main HTTP session.
"""
import logging

from typing import Any
from typing import List
from typing import Optional

from requests import Response


def check_for_errors(
    response: Response,
    allowed_http_error_status_list: Optional[List[int]] = None,
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Error check hook that raises a [HTTPError] based on response status that are greater than or equal 400.
    The status codes that will not raise a [HTTPError] can be customized via the allowed_http_error_status_list
    parameter.

    :param response:
        Response object from `requests` module.

    :param allowed_http_error_status_list:
        List of status codes that can be provided to not raise a [HTTPError].
    """
    allowed_http_error_status_list = (
        allowed_http_error_status_list if isinstance(allowed_http_error_status_list, list) else []
    )
    if all(status >= 400 for status in allowed_http_error_status_list):
        response.raise_for_status()


def log_response(response: Response, *args: Any, **kwargs: Any) -> None:
    """
    Log hook that logs the obtained response.

    :param response:
        Response object from `requests` module.
    """
    logging.debug("Request to %s returned status code %d", response.url, response.status_code)
    logging.debug("Request body: %s", response.request.body)
    logging.debug("Request headers: %s", response.request.headers)
