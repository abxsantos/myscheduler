from logging import getLogger

import telegram

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from myscheduler.services.telegram.commands import register
from myscheduler.services.telegram.commands import start
from myscheduler.services.telegram.commands import subscribe
from myscheduler.services.telegram.commands import unknown
from myscheduler.services.telegram.commands import unregister
from myscheduler.services.telegram.commands import unsubscribe
from myscheduler.settings import TELEGRAM_TOKEN

logger = getLogger(__name__)

telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
logger.info("Added [start] command handler")

register_cpf_handler = CommandHandler("register", register)
dispatcher.add_handler(register_cpf_handler)
logger.info("Added [register-cpf] command handler")

unregister_handler = CommandHandler("unregister", unregister)
dispatcher.add_handler(unregister_handler)
logger.info("Added [unregister] command handler")

subscription_handler = CommandHandler("subscribe", subscribe)
dispatcher.add_handler(subscription_handler)
logger.info("Added [subscribe] message handler")

unsubscribe_handler = CommandHandler("unsubscribe", unsubscribe)
dispatcher.add_handler(unsubscribe_handler)
logger.info("Added [unsubscribe_handler] command handler")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
logger.info("Added [unknown] message handler for unknown commands")
