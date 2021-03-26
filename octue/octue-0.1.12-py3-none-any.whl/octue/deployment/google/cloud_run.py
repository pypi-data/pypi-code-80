import base64
import json
import logging
import os
from flask import Flask, request

from octue.logging_handlers import apply_log_handler
from octue.resources.communication.google_pub_sub.service import Service
from octue.resources.communication.service_backends import GCPPubSubBackend
from octue.runner import Runner


logger = logging.getLogger(__name__)
apply_log_handler(logger, log_level=logging.INFO)

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    """Receive questions from Google Cloud Run in the form of Google Pub/Sub messages.

    :return (str, int):
    """
    envelope = request.get_json()

    if not envelope:
        return _log_bad_request_and_return_400_response("No Pub/Sub message received.")

    if not isinstance(envelope, dict) or "message" not in envelope:
        return _log_bad_request_and_return_400_response("Invalid Pub/Sub message format.")

    message = envelope["message"]

    if "data" not in message or "attributes" not in message or "question_uuid" not in message["attributes"]:
        return _log_bad_request_and_return_400_response("Invalid Pub/Sub message format.")

    project_name = envelope["subscription"].split("/")[1]
    data = json.loads(base64.b64decode(message["data"]).decode("utf-8").strip())
    question_uuid = message["attributes"]["question_uuid"]
    logger.info("Received question %r.", question_uuid)

    answer_question(project_name, data, question_uuid)
    logger.info("Analysis run and response sent for question %r.", question_uuid)
    return ("", 204)


def _log_bad_request_and_return_400_response(message):
    """Log an error return a bad request (400) response.

    :param str message:
    :return (str, int):
    """
    logger.error(message)
    return (f"Bad Request: {message}", 400)


def answer_question(project_name, data, question_uuid, deployment_configuration_path=None):
    """Answer a question from a service by running the deployed app with the deployment configuration. Either the
    `deployment_configuration_path` should be specified, or the `deployment_configuration`.

    :param str project_name:
    :param dict data:
    :param str question_uuid:
    :param str|None deployment_configuration_path:
    :return None:
    """
    deployment_configuration = {}

    if deployment_configuration_path is not None:
        with open(deployment_configuration_path) as f:
            deployment_configuration = json.load(f)

    runner = Runner(
        app_src=deployment_configuration.get("app_dir", "."),
        twine=deployment_configuration.get("twine", "twine.json"),
        configuration_values=deployment_configuration.get("configuration_values", None),
        configuration_manifest=deployment_configuration.get("configuration_manifest", None),
        output_manifest_path=deployment_configuration.get("output_manifest", None),
        children=deployment_configuration.get("children", None),
        skip_checks=deployment_configuration.get("skip_checks", False),
        log_level=deployment_configuration.get("log_level", "INFO"),
        handler=deployment_configuration.get("log_handler", None),
        show_twined_logs=deployment_configuration.get("show_twined_logs", False),
    )

    service = Service(
        id=os.environ["SERVICE_ID"],
        backend=GCPPubSubBackend(project_name=project_name, credentials_environment_variable=None),
        run_function=runner.run,
    )

    service.answer(data=data, question_uuid=question_uuid)
