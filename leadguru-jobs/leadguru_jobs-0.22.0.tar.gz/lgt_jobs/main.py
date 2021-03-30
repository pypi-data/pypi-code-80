import json
import sys
import time
from lgt_jobs import BackgroundJobRunner, jobs_map
from lgt.common.python.pubsub.pubsubfactory import PubSubFactory
from lgt.common.python.lgt_logging import log

from lgt_jobs import env

def run_background_job(message):
    data = json.loads(message.data)
    log.info(f"[JOB]: {data} [START]")
    try:
        BackgroundJobRunner.run(jobs_map=jobs_map, data=data)
        message.ack()
        log.info(f"[JOB]: {data} [FINISHED]")
    except Exception as e:
        import traceback
        log.error(f"[ERROR][JOB]: {data} [DATA]: {json.dumps(data)} [ERROR] {traceback.format_exception(*sys.exc_info())} ")

if __name__ == '__main__':
    factory = PubSubFactory(env.project_id)
    factory.create_topic_if_doesnt_exist(env.background_jobs_topic)
    factory.create_subscription_if_doesnt_exist(env.background_jobs_subscriber, env.background_jobs_topic)
    bot_subscription_path = factory.get_subscription_path(env.background_jobs_subscriber, env.background_jobs_topic)

    factory.subscriber.subscribe(bot_subscription_path, callback=run_background_job)
    print(f'Listening for messages on {bot_subscription_path}')
    while True:
        time.sleep(1)