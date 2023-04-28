import logging

import configargparse
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


def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
    )


def parse_args():
    parser = configargparse.ArgParser()
    parser.add_argument(
        '--debug',
        help='debug mode',
        action='store_true',
        env_var='DVMN_BOT__DEBUG',
    )
    parser.add_argument(
        '--tlgrm-creds',
        help='telegram bot access token',
        env_var='DVMN_BOT__TELEGRAM_CREDS',
        required=True,
    )

    return parser.parse_args()


def main():
    options = parse_args()
    logging.basicConfig(level=logging.INFO)
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    updater = Updater(token=options.tlgrm_creds)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), echo)
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
