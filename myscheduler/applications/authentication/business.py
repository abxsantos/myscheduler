import logging

from typing import Callable

from django.db import DatabaseError
from django.db import transaction

from django_q.models import Schedule
from django_q.tasks import async_task

from myscheduler.applications.authentication.hooks import cpf_validation_hook
from myscheduler.applications.authentication.models import Client
from myscheduler.services.four_devs import request_cpf_validation

logger = logging.getLogger(__name__)


def validate_client_cpf(client_id: str) -> bool:
    """
    Validate the cpf from the client using the 4devs API.

    """
    client = Client.objects.get(id=client_id)
    response = request_cpf_validation(cpf=client.cpf)

    if isinstance(response, str) and "verdadeiro" in response.lower():
        logger.info(f"The cpf validation result was {response}, setting the `Client` status to VALID!")
        client.cpf_validation_status = Client.CPFValidationStatus.VALID
    else:
        logger.warning(f"The cpf validation result was invalid, setting the `Client` status to INVALID!")
        client.cpf_validation_status = Client.CPFValidationStatus.INVALID
    with transaction.atomic():
        client.save()
    client.refresh_from_db()
    return client.has_valid_cpf


def register(telegram_send_message_callback: Callable, client_id: str, username: str, chat_id: str, cpf: str):
    """
    Registers a CPF to a `Client` using the `chat_id` and `bot_name` from the telegram API incoming update.
    As soon as the `Client` is created it will send a message informing the id.

    This will also create a `Task` that will validate the user CPF in the background using the 4devs API.

    After validating, it will send a message to the user informing if the provided CPF is valid or not.

    """
    try:
        with transaction.atomic():
            created_client, has_created = Client.objects.get_by_id_or_create(
                id=client_id,
                username=username,
                cpf=cpf,
            )
            if has_created:
                async_task(
                    func=f"{__name__}.validate_client_cpf",
                    client_id=created_client.id,
                    group=f"validate_cpf_{created_client.id}",
                    hook=f"{cpf_validation_hook.__module__}.{cpf_validation_hook.__name__}",
                )
    except DatabaseError as database_error:
        logger.exception(f"There was a problem creating the `Client` entry!", exc_info=database_error)
        created_client = None
    telegram_send_message_callback(
        chat_id=chat_id,
        text=f"Your created `id` is {created_client.id} and "
        f"your cpf validation status is {created_client.cpf_validation_status}"
        if created_client
        else {"Couldn't create a registration entry!"},
    )


def unregister(chat_id: str, client_id: str, telegram_send_message_callback: Callable):
    """
    Unregisters a `Client` using the chat_id and bot_name from the telegram API incoming update.

    This will also delete an activity `Schedule` attached to the user and any cpf validation tasks related to it.

    """
    try:
        with transaction.atomic():
            Schedule.objects.filter(
                name=f"activity_subscription_{client_id}",
            ).delete()
            Client.objects.filter(id=client_id).delete()
        telegram_send_message_callback(chat_id=chat_id, text=f"Your account was successfully unregistered!")
    except DatabaseError as database_error:
        logger.exception(f"There was a problem deleting the `Client` entry!", exc_info=database_error)
        telegram_send_message_callback(
            chat_id=chat_id, text=f"There was a problem unregistering your account! Try again!"
        )
