from microservice_template_core.tools.flask_restplus import api
from flask_restx import Resource
import traceback
from microservice_template_core.tools.logger import get_logger
from flask import request

logger = get_logger()
ns = api.namespace('collector', description='Harp Voice Notification endpoints')


@ns.route('/')
class NotificationStatus(Resource):
    @staticmethod
    @api.response(200, 'Notification has been created')
    @api.response(500, 'Unexpected error on backend side')
    def get():
        """
        Get status of existing Voice Notification in Twilio
        """

        logger.info(
            msg=f"Received request to get status of existing Voice notification via Twilio",
            extra={'tags': {}}
        )
        try:
            status = 'TBD'
            return {'status': status}, 200
        except Exception as exc:
            logger.critical(
                msg=f"Can`t Collect \nException: {str(exc)} \nTraceback: {traceback.format_exc()}",
                extra={'tags': {}})
            return {'msg': 'Exception raised. Check logs for additional info'}, 500

