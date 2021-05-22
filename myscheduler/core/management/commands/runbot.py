from logging import getLogger
from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser

from myscheduler.services.telegram.bot import updater

logging = getLogger(__name__)


class Command(BaseCommand):
    help = "Starts the telegram bot"

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Adds the stop argument that will stop the telegram bot
        """
        parser.add_argument("-s", "--stop", action="store_true", help="Stops the telegram bot")

    def handle(self, *args: Any, **kwargs: Any) -> None:
        """
        Main handler that ill start pooling information from the telegram bot
        """
        is_stop = kwargs.get("stop", False)
        logging.info("Started telegram bot!" if not is_stop else "Stopping telegram bot!")
        updater.start_polling() if not is_stop else updater.stop()
