from typing import TypedDict

from requests import HTTPError

from myscheduler.core.http.session import requests_session
from myscheduler.services.exceptions import FailureToRetrieveActivity


class BoredApiSuccessfulResponseBody(TypedDict):
    activity: str
    type: str
    participants: int
    price: int
    link: str
    key: int
    accessibility: float


def get_activity() -> BoredApiSuccessfulResponseBody:
    """
    Makes a GET request to `boredapi` activity resource.

    Returns on status 200:
    {
        "activity": "Learn a new recipe",
        "accessibility": 0.05,
        "type":"cooking",
        "participants": 1,
        "price": 0
    }

    Raises on status >= 4xx:
    Will raise a `FailureToRetrieveActivity`
    API exception, containing the retrieved status code.
    """
    try:
        with requests_session() as request:
            response = request.get(url="https://www.boredapi.com/api/activity/")
        return response.json()
    except HTTPError as http_error:
        raise FailureToRetrieveActivity(
            message="There was a failure to retrieve the activity! "
            f"status_code: {http_error.response.status_code}, body: {http_error.response.body}"
        )
