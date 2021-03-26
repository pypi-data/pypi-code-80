import os

project_id = os.environ.get('PROJECT_ID')
slack_login_url = os.environ.get('SLACK_LOGIN_URL')
background_jobs_topic = os.environ.get('BACKGROUND_JOBS_TOPIC')
background_jobs_subscriber = os.environ.get('BACKGROUND_JOBS_SUBSCRIBER')
mongo_connection_string = os.environ.get('MONGO_CONNECTION_STRING')
