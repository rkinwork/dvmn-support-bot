import logging
import pathlib

import configargparse

import telegram_bot
import vk_bot
from dialog_flow import DialogFlow
from telegram_handler import TelegramHandler

logger = logging.getLogger(__name__)

DEFAULT_TRAIN_SOURCE = pathlib.Path(__file__).parent / 'train.json'


def parse_args():
    parser = configargparse.ArgParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        '--debug',
        help='debug mode',
        action='store_true',
        env_var='DVMN_BOT__DEBUG',
    )
    group.add_argument(
        '--train-bot',
        help='run script in train mode. And terminate program',
        env_var='DVMN_BOT__TRAIN_MODE',
        action='store_true',
    )

    group.add_argument(
        '--run-telegram-bot',
        help='run telegram bot',
        env_var='DVMN_BOT__TELEGRAM_MODE',
        action='store_true',
    )

    group.add_argument(
        '--run-vk-bot',
        help='run vk bot',
        env_var='DVMN_BOT__VK_MODE',
        action='store_true',
    )

    parser.add_argument(
        '--tg_token',
        help='telegram bot access token',
        env_var='DVMN_BOT__TELEGRAM_CREDS',
    )
    parser.add_argument(
        '--vk_token',
        help='vk bot access token',
        env_var='DVMN_BOT__VK_CREDS',
    )
    parser.add_argument(
        '--dialog_flow_id',
        help='dialog flow project id',
        env_var='DVMN_BOT__DIALOG_FLOW_ID',
        required=True,
    )
    parser.add_argument(
        '--admin-chat-id',
        help='telegram chat id',
        env_var='DVMN_BOT__ADMIN_CHAT_ID',
        required=True,
    )

    parser.add_argument(
        '--train-path',
        help='custom training file path',
        env_var='DVMN_BOT__TRAIN_PATH',
    )

    return parser.parse_args()


def main():
    logging.basicConfig()
    options = parse_args()
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if options.debug:
        root_logger.setLevel(logging.DEBUG)

    telegram_error_hndlr = TelegramHandler(
        token=options.tg_token,
        admin_chat_id=options.admin_chat_id,
    )
    telegram_error_hndlr.setLevel(level=logging.ERROR)
    root_logger.addHandler(telegram_error_hndlr)
    telegram_info_hndlr = TelegramHandler(
        token=options.tg_token,
        admin_chat_id=options.admin_chat_id,
    )
    telegram_info_hndlr.setLevel(level=logging.INFO)
    logger.addHandler(hdlr=telegram_info_hndlr)

    dialog_flow = DialogFlow(
        project_id=options.dialog_flow_id,
    )

    if options.train_bot:
        train_source_path = DEFAULT_TRAIN_SOURCE
        if options.train_path is not None:
            train_source_path = pathlib.Path(options.train_path)
        dialog_flow.train(train_source=train_source_path)
        return

    if options.run_telegram_bot:
        logger.info('Execution of telegram support started')
        telegram_bot.run(
            token=options.tg_token,
            intent_detector=dialog_flow.detect_intent_texts,
        )
        return

    if options.run_vk_bot:
        logger.info('Execution of vk support started')
        try:
            vk_bot.run(
                token=options.vk_token,
                intent_detector=dialog_flow.detect_intent_texts,
            )
        except Exception as exception:
            logger.error(msg=exception)
            raise


if __name__ == '__main__':
    main()
