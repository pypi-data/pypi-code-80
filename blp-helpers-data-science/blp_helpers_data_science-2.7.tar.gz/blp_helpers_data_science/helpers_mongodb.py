import pymongo
from pymongo.errors import OperationFailure
import logging
import os


def get_mongo_collection():

    logger = logging.getLogger(__name__)

    mongodb_user = False
    mongodb_pw = False
    mongodb_port = False
    mongodb_host = False
    mongodb_db_name = False
    mongodb_collection_name = False

    env_vars_available = False
    mongodb_connected = False
    db_available = False
    mongo_client = False
    mongo_collection = False

    try:
        mongodb_user = os.environ['MONGODB_USER']
        mongodb_pw = os.environ['MONGODB_PW']
        mongodb_port = os.environ['MONGODB_PORT']
        mongodb_host = os.environ['MONGODB_HOST']
        mongodb_db_name = os.environ['MONGODB_DB']
        mongodb_collection_name = os.environ['MONGODB_COLLECTION']
        env_vars_available = True
        logger.info("env_vars_available available")
    except KeyError as e:
        logger.error('issues at os.environ {}'.format(e))

    if env_vars_available:
        try:
            mongo_client = pymongo.MongoClient(
                "mongodb://{}:{}@{}:{}/?authSource={}&readPreference=primary&appname=MongoDB%20Compass&ssl=false".format(
                    mongodb_user, mongodb_pw, mongodb_host, mongodb_port, mongodb_db_name
                )
            )
            mongodb_connected = True
            logger.info("mongodb_connected")
        except ValueError as e:
            logger.error('issues at mongo_client {}'.format(e))

    if mongodb_connected:
        try:
            mongo_client.list_database_names().index(mongodb_db_name)
            template = 'analytics/analytics_topic_analysis.html'
            db_available = True
            logger.info("list_database_names available")
        except ValueError as e:
            logger.error('The DB: {} is not available. Error Msg.: {}'.format(mongodb_db_name, e))
        except OperationFailure as e:
            logger.error('cannot authenticate to db'.format(mongodb_db_name, e))

    if db_available:
        # no error handling necessary
        mongo_db = mongo_client[mongodb_db_name]
        mongo_collection = mongo_db[mongodb_collection_name]
        logger.info("opened collection")

    return mongo_collection
