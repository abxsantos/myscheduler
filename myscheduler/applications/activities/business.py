import logging

from typing import Callable

from django.db import DatabaseError
from django.db import transaction

from django_q.models import Schedule
from django_q.tasks import schedule

from myscheduler.applications.activities.hooks import dispatch_activity_hook
from myscheduler.applications.activities.models import Activity
from myscheduler.applications.authentication.models import Client
from myscheduler.services.bored_api import get_activity

logger = logging.getLogger(__name__)


def send_activity_to_user(chat_id: int, bot_username: str) -> str:
    activity_response = get_activity()
    Activity.objects.create(
        client_id=f"{chat_id}-{bot_username}",
        key=activity_response.get("key"),
        activity=activity_response.get("activity"),
        type=activity_response.get("type"),
        participants=activity_response.get("participants"),
        price=activity_response.get("price"),
        link=activity_response.get("link"),
    )
    return activity_response.get("activity")


def subscribe(client_id: str, telegram_send_message_callback: Callable, chat_id: str, bot_name: str) -> None:
    """
    Subscribe the current user, creating a `Schedule` that will send activities hourly based on the bored API.

    """
    client = Client.objects.get_or_none(id=client_id)
    if client and client.is_subscribed:
        telegram_send_message_callback(chat_id=chat_id, text="You're already subscribed!")
        return
    try:
        with transaction.atomic():
            client.is_subscribed = True
            client.save()
            schedule(
                func=f"{send_activity_to_user.__module__}.{send_activity_to_user.__name__}",
                chat_id=chat_id,
                bot_username=bot_name,
                schedule_type=Schedule.HOURLY,
                name=f"activity_subscription_{client_id}",
                hook=f"{dispatch_activity_hook.__module__}.{dispatch_activity_hook.__name__}",
            )
            telegram_send_message_callback(
                chat_id=chat_id, text="Subscribed to activities! A new one will be sent every hour!"
            )
    except DatabaseError as database_error:
        logger.exception(f"There was a problem creating a subscription!", exc_info=database_error)
        telegram_send_message_callback(chat_id=chat_id, text="There was a problem subscribing! Try again later!")


def unsubscribe(client_id: str, telegram_send_message_callback: Callable, chat_id: str) -> None:
    """
    Unsubscribe the current user, removing the activities `Schedule` that is attached.

    """
    activities_subscription_schedule = Schedule.objects.filter(
        func=f"{send_activity_to_user.__module__}.{send_activity_to_user.__name__}",
        name=f"activity_subscription_{client_id}",
        schedule_type=Schedule.HOURLY,
    )
    with transaction.atomic():
        activities_subscription_schedule.delete()
    telegram_send_message_callback(chat_id=chat_id, text="Unsubscribed to activities!")
