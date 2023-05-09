import os
import logging

from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello',
    )


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg="Exception while handling an update:",
        exc_info=context.error,
    )


class Dialog:
    def __init__(
            self,
            intent_detector,

    ):
        self._intent_detector = intent_detector

    def handler(self, update: Update, context: CallbackContext):
        response, _ = self._intent_detector(
            session_id=update.effective_user.id,
            text=update.message.text,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
        )


def run(token: str, intent_detector):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (~Filters.command),
            Dialog(intent_detector=intent_detector).handler),
    )
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
