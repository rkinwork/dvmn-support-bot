import logging
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

log = logging.getLogger(__name__)
VK_LISTEN_ATTEMPTS = 5
VK_LISTEN_TIMEOUT = 60


def send_answer(vk_api, event, intent_detector):
    response, is_fallback = intent_detector(
        session_id=event.user_id,
        text=event.text,
    )
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response,
            random_id=random.randint(1, 1000),
        )


def run(token: str, intent_detector):
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    session = VkLongPoll(vk_session)
    events = session.listen()
    attempts_cnt = 0
    while True:
        attempts_cnt += 1
        try:
            event = next(events)
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
        ) as api_except:
            if attempts_cnt > VK_LISTEN_ATTEMPTS:
                log.warning('Attempts to get event from VK api finished')
                raise api_except
            log.warning('Problems with VK Long Polling API %s', api_except)
            continue
        except StopIteration:
            log.warning('restarting VK poller')
            events = session.listen()
            continue

        attempts_cnt = 0
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(
                vk_api=vk_api,
                event=event,
                intent_detector=intent_detector,
            )
