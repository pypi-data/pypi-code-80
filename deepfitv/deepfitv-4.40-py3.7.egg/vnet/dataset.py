import boto3
from boto3 import Session
from io import BytesIO
import numpy as np

def load(imageType):
    client = boto3.client('s3') #low-level functional API
    obj = client.get_object(Bucket='vlifedata', Key='Vlife_3.0/Ruby/GAN/'+imageType+".npy")
    return np.load(BytesIO(obj['Body'].read()),allow_pickle=True) 
