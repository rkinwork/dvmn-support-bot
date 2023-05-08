import logging
from functools import partial

import configargparse

import telegram_bot
import dialog_flow
import vk_bot

logger = logging.getLogger(__name__)


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

    return parser.parse_args()


def main():
    options = parse_args()
    logging.basicConfig(level=logging.INFO)
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    df_id = options.dialog_flow_id
    if options.train_bot:
        dialog_flow.train(df_id)
        return

    intent_detector = partial(
                dialog_flow.detect_intent_texts,
                project_id=df_id,
                language_code='ru',
            )

    if options.run_telegram_bot:
        telegram_bot.run(
            token=options.tg_token,
            intent_detector=intent_detector,
        )
        return

    if options.run_vk_bot:
        vk_bot.run(
            token=options.vk_token,
            intent_detector=intent_detector,
        )


if __name__ == '__main__':
    main()
