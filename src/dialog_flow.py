import json
import pathlib
import logging

from google.cloud import dialogflow

logger = logging.getLogger(__name__)


def train(dialog_flow_id: str):
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


def detect_intent_texts(project_id: str,
                        session_id: str,
                        text: str,
                        language_code: str
                        ) -> (str, bool):
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
    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback
