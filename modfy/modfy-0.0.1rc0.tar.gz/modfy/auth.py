from Crypto.Cipher import PKCS1_OAEP
import requests
from modfy.config import Config

import json
from Crypto.PublicKey import RSA
import base64

# TODO Proper Error Handling


class Auth:

    def __init__(self, token, secretToken):
        self.token = token
        self.secretToken = secretToken
        self.config = Config()
        self.SERVER_URL = self.config.SERVER_URL

    def __getEphemeral(self):
        token = self.token

        url = self.SERVER_URL + '/api/key/ephemeral'

        try:
            response = requests.post(url, json={'token': token})
            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            print('Error getting ephemeral token', e)
            raise SystemExit(e)

    def __encryptSecret(self, publicKey):
        key = RSA.importKey(str.encode(publicKey))
        cipher = PKCS1_OAEP.new(key)

        encryptedToken = base64.b64encode(
            cipher.encrypt(str.encode(self.secretToken)))

        return encryptedToken

    def __validateSecret(self, encryptedToken, keyName):
        url = self.SERVER_URL + '/api/secret/validate'

        try:
            encrypted = encryptedToken.decode()
            response = requests.post(url, json={
                                     'encryptedToken': encrypted, 'keyName': keyName, 'token': self.token})
            response.raise_for_status()
            data = response.json()
            return data['oneTimeToken']
        except requests.exceptions.RequestException as e:
            print('Error validating secret', e, e.request.body)
            raise SystemExit(e)

    def getOneTimeToken(self):
        empheralData = self.__getEphemeral()
        encryptedToken = self.__encryptSecret(empheralData['publicKey'])
        oneTimeToken = self.__validateSecret(
            encryptedToken, empheralData['keyName'])
        return oneTimeToken

    def verifyOneTimeToken(self, token):
        url = self.SERVER_URL + '/api/onetime/verify'
        try:
            response = requests.get(url, headers={'onetime-token': token})
            data = response.json()
            response.raise_for_status()
            return {'isValid': True, 'test': data['test']}
        except requests.exceptions.RequestException as e:
            print('Error verifying token', e)
            raise SystemExit(e)

    def consumeOneTimeToken(self, token):
        url = self.SERVER_URL + '/api/onetime/consume'
        try:
            response = requests.get(url, headers={'onetime-token': token})
            data = response.json()
            response.raise_for_status()
            return data['teamId']
        except requests.exceptions.RequestException as e:
            print('Error verifying token', e)
            raise SystemExit(e)
