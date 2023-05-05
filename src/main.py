import json
import logging
import pathlib

import configargparse
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


class Dialog:
    def __init__(
            self,
            project_id: str,
            language_code: str = 'ru',
    ):
        self._project_id = project_id
        self._language_code = language_code

    def handler(self, update: Update, context: CallbackContext):
        response = detect_intent_texts(
            project_id=self._project_id,
            session_id=update.effective_user.id,
            text=update.message.text,
            language_code=self._language_code,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
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
        '--train-bot',
        help='run script in train mode. And terminate program',
        action='store_true',
    )
    parser.add_argument(
        '--tlgrm-creds',
        help='telegram bot access token',
        env_var='DVMN_BOT__TELEGRAM_CREDS',
        required=True,
    )
    parser.add_argument(
        '--dialog_flow_id',
        help='dialog flow project id',
        env_var='DVMN_BOT__DIALOG_FLOW_ID',
        required=True,
    )

    return parser.parse_args()


def detect_intent_texts(project_id: str,
                        session_id: str,
                        text: str,
                        language_code: str
                        ) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    logger.debug('Session path: {}'.format(session))

    query_input = dialogflow.QueryInput(
        text=dialogflow.TextInput(
            text=text,
            language_code=language_code,
        )
    )

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input,
        }
    )

    logger.debug("Query text: {}".format(response.query_result.query_text))
    logger.debug(
        "Detected intent: {} (confidence: {})".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    logger.debug("Fulfillment text: {}".format(
        response.query_result.fulfillment_text,
    )
    )
    return response.query_result.fulfillment_text


def train_dialog_flow(dialog_flow_id: str):
    content = json.loads(
        (pathlib.Path(__file__).parent / 'train.json').read_text()
    )
    for name, train_opts in content.items():
        create_intent(
            project_id=dialog_flow_id,
            display_name=name,
            training_phrases_parts=train_opts['questions'],
            message_texts=(train_opts['answer'],),
        )


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts,
):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(
        request={
            "parent": parent,
            "intent": intent,
            "language_code": 'ru',
        },
    )

    logger.debug("Intent created: {}".format(response))


def main():
    options = parse_args()
    logging.basicConfig(level=logging.INFO)
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    if options.train_bot:
        train_dialog_flow(options.dialog_flow_id)
        return
    updater = Updater(token=options.tlgrm_creds)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (~Filters.command),
            Dialog(options.dialog_flow_id).handler),
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
