import boto3
from boto3 import Session
from io import BytesIO
import numpy as np

def load(imageType):
    client = boto3.client('s3',aws_access_key_id="AKIAYR7USY6BBSJ54X52",aws_secret_access_key="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") #low-level functional API
    obj = client.get_object(Bucket='vlifedata', Key='Vlife_3.0/Ruby/GAN/'+imageType+".npy")
    return np.load(BytesIO(obj['Body'].read()),allow_pickle=True)
