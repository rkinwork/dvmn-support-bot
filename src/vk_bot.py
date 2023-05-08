import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(vk_api, event):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


def bot(vk_api, event, intent_detector):
    response = intent_detector(
        session_id=event.user_id,
        text=event.text,
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=response,
        random_id=random.randint(1, 1000)
    )


def run(token: str, intent_detector):
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot(
                vk_api=vk_api,
                event=event,
                intent_detector=intent_detector,
            )
