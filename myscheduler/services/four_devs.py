from requests.models import HTTPError

from myscheduler.core.http.session import requests_session
from myscheduler.services.exceptions import FailureToRetrieveCPFValidation


def request_cpf_validation(cpf: str) -> str:
    """
    Makes a POST request to `4devs.com.br` passing the `cpf`
    in the payload body.

    Returns on status 200:
    12595312790 - Verdadeiro
    """
    try:
        with requests_session() as request:
            response = request.post(
                url="https://www.4devs.com.br/ferramentas_online.php",
                headers={
                    "Accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest",
                    "Origin": "https://www.4devs.com.br",
                    "Referer": "https://www.4devs.com.br/validador_cpf",
                },
                data=f"acao=validar_cpf&txt_cpf={cpf}",
            )
        return response.text
    except HTTPError as http_error:
        error_response = http_error.response
        raise FailureToRetrieveCPFValidation(
            message="Failed to retrieve the cpf validation. "
            f"status_code: {error_response.status_code} text: {error_response.text}"
        )
