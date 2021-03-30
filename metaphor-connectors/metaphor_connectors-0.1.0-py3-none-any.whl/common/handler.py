import json
import logging
from typing import Type

from metaphor.common.extractor import RunConfig, BaseExtractor
from metaphor.common.response import LambdaResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_api(
    event, context, runConfig: Type[RunConfig], extractor: Type[BaseExtractor]
):
    params = json.loads(event["body"]) if "body" in event else event["params"]
    for parameter in runConfig.parameters():
        if parameter not in params:
            return {"statusCode": 422, "body": f"Missing param: ${parameter}"}

    config = runConfig.build(params)

    try:
        actor = extractor()
        actor.run(config=config)
    except Exception as e:
        logger.exception(str(e))
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": json.dumps(params)}
