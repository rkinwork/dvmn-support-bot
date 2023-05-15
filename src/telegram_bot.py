import logging

from telegram import Update
from telegram.ext import (CallbackContext,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          Updater,
                          )

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello',
    )


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg='Exception while handling an update:',
        exc_info=context.error,
    )


def get_dialog_handler(intent_detector):
    def handler(update: Update, context: CallbackContext):
        response, _ = intent_detector(
            session_id=update.effective_user.id,
            text=update.message.text,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
        )

    return handler


def run(token: str, intent_detector):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (~Filters.command),
            get_dialog_handler(intent_detector),
        ),
    )
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
