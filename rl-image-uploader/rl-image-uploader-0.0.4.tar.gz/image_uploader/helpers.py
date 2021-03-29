from base64 import b64decode, b64encode
from hashlib import md5
import json
import logging

import boto3
from parse import parse
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_image_data(url):
    response = requests.get(url)
    response.raise_for_status()
    response.raw.decode_content = True
    return response.content


def upload_image_from_url(
        bucket,
        key,
        url
):
    image_data = _get_image_data(url)
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Body=image_data, Bucket=bucket, Key=key)
    except s3_client.exceptions.ClientError:
        logger.exception('Error uploading image')
        return False
    return True


def upload_image_from_data(
        bucket,
        key,
        image_data,
):
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Body=image_data, Bucket=bucket, Key=key)
    except s3_client.exceptions.ClientError:
        logger.exception('Error uploading image')
        return False
    return True


def encode_image_url(
        resource_type,
        image_url,
        image_domain,
        image_bucket,
        app_id,
        image_edits
):
    image_hash = md5(image_url.encode('utf-8')).hexdigest()
    image_metadata = {
        'bucket': image_bucket,
        'key': '{}/{}/{}'.format(
            app_id,
            resource_type,
            image_hash
        ),
    }
    if image_edits:
        image_metadata['edits'] = image_edits
    encoded_metadata = b64encode(json.dumps(image_metadata).encode('utf-8'))
    return '{}/{}'.format(image_domain, encoded_metadata.decode('utf-8'))


def decode_image_url(
        image_domain,
        image_url,
):
    parsed_image_url = parse(
        '{}/{}'.format(
            image_domain, '{encoded_image_info}'
        ),
        image_url
    )
    if not parsed_image_url:
        return None
    decoded_image_info = json.loads(b64decode(parsed_image_url['encoded_image_info'].encode('utf-8')))
    return decoded_image_info
