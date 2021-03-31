import slackbot
import json
import requests
from datetime import datetime

def post_message(message):
    webhook_url = "https://hooks.slack.com/services/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"

    data = [{"type": "section",
         "text": {
              "type": "mrkdwn",
              "text": f"{message}"
          }}]
    slack_data = json.dumps({'text': 'message from noti_bot',
        'blocks': data})
    response = requests.post(webhook_url,
                             data=slack_data,
                             headers={'Content-type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
        f'Request to slackbot returned an error {response.status_code}\n \
        the response is {response.text}')


def post_job_done(work_name):
    webhook_url = "https://hooks.slack.com/services/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"

    data = [{"type": "section",
             "text": {
                 "type": "mrkdwn",
                 "text": f"{work_name} done at {datetime.now().strftime(r'%m%d_%H%M')}"
             }}]
    slack_data = json.dumps({'text': f"{work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n {work_name} job-done!!!!! \n",
        'blocks': data})
    response = requests.post(webhook_url,
                             data=slack_data,
                             headers={'Content-type': 'application/json'}
                             )
    if response.status_code != 200:
        raise ValueError(
            f'Request to slackbot returned an error {response.status_code}\n \
        the response is {response.text}')
