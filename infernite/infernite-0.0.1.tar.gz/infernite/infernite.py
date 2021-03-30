import requests
import json
import io


class Infernite:
    def __init__(self, token):
        self.token = token
        self.api = "https://infernite.ai/predictions"

    def predict(self, body):
        files = {}
        if "image" in body:
            file_path = body["image"]
            if file_path.find("https://") == 0 or file_path.find("http://") == 0:
                data = requests.get(file_path, stream=True).content
                files["image"] = io.BytesIO(data)
            else:
                files["image"] = open(file_path, "rb")

            del body["image"]

        headers = {'Token': self.token}

        response = requests.post(
            self.api, files=files, data=body, headers=headers)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise RuntimeError("Status code {}: {}".format(response.status_code, response.text))
