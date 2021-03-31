from decouple import config


class Config:

    def __init__(self):
        self.dev = config('DEV', default="False") == "True"

    @property
    def API_URL(self):
        if (self.dev):
            return 'http://localhost:80'
        else:
            return 'https://mila.modfy.video'

    @property
    def SERVER_URL(self):
        if (self.dev):
            return 'http://localhost:5000'
        else:
            return 'https://server.modfy.video'
