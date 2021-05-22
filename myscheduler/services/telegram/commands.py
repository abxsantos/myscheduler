from logging import getLogger

from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext

import myscheduler.applications.activities.business

from myscheduler.applications import activities
from myscheduler.applications import authentication
from myscheduler.applications.authentication import business
from myscheduler.core.utilities.helpers import safe_list_get

logger = getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """
    Demonstrate how to use the main bot commands
    """
    logger.info(
        f"Bot `{update.message.chat.bot.username}` "
        f"chat id {update.message.chat_id} "
        "received a `start` command "
        f"from user `{update.message.chat.username}`"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode=ParseMode.MARKDOWN_V2,
        text="To create an user, use the `register` command with a `cpf` "
        "\n\n**Example**"
        "\n`\/register_cpf 11122233344`"
        "\n To unregister use the `\/unregister` command\!"
        "\n\n You can also subscribe to receive an activity to do every "
        "hour with the `subscribe` command "
        "\n\n**Example**"
        "\n`\/subscribe`"
        "\n To unsubscribe use the `\/subscribe` command\!",
    )


def register(update: Update, context: CallbackContext) -> None:
    """
    Registers a CPF to a `Client` using the `chat_id` and `bot_name` from the telegram API incoming update.
    As soon as the `Client` is created it will send a message informing the id.

    This will also create a `Task` that will validate the user CPF in the background using the 4devs API.

    After validating, it will send a message to the user informing if the provided CPF is valid or not.

    """
    bot_name = update.message.chat.bot.username
    username = update.message.chat.username
    chat_id = update.message.chat_id
    logger.info(
        f"Bot `{bot_name}` "
        f"chat id {update.message.chat_id} "
        "received a `register-cpf` command "
        f"from user `{username}`"
    )
    authentication.business.register(
        cpf=safe_list_get(list_=context.args, index=0, default=""),
        chat_id=str(chat_id),
        client_id=f"{chat_id}-{bot_name}",
        username=username,
        telegram_send_message_callback=context.bot.send_message,
    )


def unregister(update: Update, context: CallbackContext) -> None:
    """
    Unregisters a `Client` using the chat_id and bot_name from the telegram API incoming update.

    This will also delete an activity `Schedule` attached to the user and any cpf validation tasks related to it.

    """
    bot_name = update.message.chat.bot.username
    username = update.message.chat.username
    chat_id = update.message.chat_id
    logger.info(
        f"Bot `{bot_name}` " f"chat id {chat_id} " "received an `unregister` command " f"from user `{username}`"
    )
    authentication.business.unregister(
        chat_id=str(chat_id),
        client_id=f"{chat_id}-{bot_name}",
        telegram_send_message_callback=context.bot.send_message,
    )


def subscribe(update: Update, context: CallbackContext) -> None:
    """
    Subscribe the current user, creating a `Schedule` that will send activities hourly based on the bored API.

    """
    bot_name = update.message.chat.bot.username
    username = update.message.chat.username
    chat_id = update.message.chat_id
    logger.info(f"Bot `{bot_name}` " "received a `subscribe` message " f"from user `{username}`")
    activities.business.subscribe(
        chat_id=str(chat_id),
        bot_name=bot_name,
        client_id=f"{chat_id}-{bot_name}",
        telegram_send_message_callback=context.bot.send_message,
    )


def unsubscribe(update: Update, context: CallbackContext) -> None:
    """
    Unsubscribe the current user, removing the activities `Schedule` that is attached.

    """
    bot_name = update.message.chat.bot.username
    chat_id = update.effective_chat.id
    logger.info(f"Bot `{bot_name}` " "received a `subscribe` message " f"from user `{update.message.chat.username}`")
    activities.business.unsubscribe(
        chat_id=str(chat_id),
        client_id=f"{chat_id}-{bot_name}",
        telegram_send_message_callback=context.bot.send_message,
    )


def unknown(update: Update, context: CallbackContext) -> None:
    """
    To improve the user feedback for unrecognizable commands

    """
    logger.info(
        f"Bot `{update.message.chat.bot.username}` "
        "received an `unknown` command "
        f"from user `{update.message.chat.username}`"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
