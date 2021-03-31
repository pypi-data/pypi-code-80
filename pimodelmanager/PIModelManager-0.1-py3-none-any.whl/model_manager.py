import io
import json
import logging
from pathlib import Path
from typing import ClassVar, Dict, List
from zipfile import ZipFile

import requests
from natsort import natsorted

from PIModelManager.pandora_model import PandoraModel

logger = logging.getLogger("PIModelManager")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
ch.setFormatter(formatter)

logger.addHandler(ch)


class ModelManager:
    """Singleton class that manages ML models"""

    __instance: ClassVar[object] = None

    _credentials: ClassVar[Dict[str, str]] = {}
    _container: ClassVar[str] = None
    _login_url: ClassVar[str] = None
    _get_files_url: ClassVar[str] = None
    _download_file_url: ClassVar[str] = None
    
    _available_models: ClassVar[List[PandoraModel]] = []
    _downloaded_models: ClassVar[List[PandoraModel]] = []
    _loaded_models: ClassVar[List[PandoraModel]] = []

    def __new__(cls):
        if ModelManager.__instance is None:
            ModelManager.__instance = object.__new__(cls)
        return ModelManager.__instance

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token

        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r

    @classmethod
    def set_credentials(
        cls,
        grant_type: str,
        client_id: str,
        client_secret: str,
        scope: str,
        container: str,
        login_url: str,
        get_files_url: str,
        download_file_url: str
    ):
        """Set credentials for the ModelManager

        Args:
            grant_type (str): Type of grant
            client_id (str): The consumer key
            client_secret (str): The consumer secret
            scope (str): The control scope
            container (str): The name of the storage container
            login_url (str): The sts login url
            get_files_url (str): The URL for getting a list of available files in a container. Put variables in curly brackets.
            download_file_url (str): The URL for downloading a specific file from a container. Put variables in curly brackets.
        """
        
        if(not all([grant_type, client_id, client_secret, scope, container, login_url, get_files_url, download_file_url])):
            raise Exception("Argument is empty or None.")

        cls._credentials = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        }

        cls._container = container
        cls._login_url = login_url
        cls._get_files_url = get_files_url
        cls._download_file_url = download_file_url

    @classmethod
    def __authenticate(cls):
        """Authenticate with the server.

        Raises:
            Exception: In case the credentials are not previously set using 'set_credentials' method.

        Returns:
            str: Access token
        """
        if not cls._credentials or not cls._login_url:
            raise Exception("Credentials not set. Use method set_credentials.")

        # Authentication request
        response = requests.post(cls._login_url, data=cls._credentials)
        if response.status_code == 200:
            result = json.loads(response.text)

            logger.info("Authentication successful")
            return result["access_token"]

        return None

    @classmethod
    def __get_files(cls, token: str):
        """Returns a list of available model files.

        Args:
            token (str): Authentication bearer token

        Returns:
            List[str]: List of all available model files
        """
        url = cls._get_files_url.replace("{container}", cls._container)
        response = requests.get(url, auth=cls.BearerAuth(token))
        if response.status_code == 200:
            return [dict(x)["name"] for x in json.loads(response.text)]
        else:
            return []

    @classmethod
    def download_model(cls, language: str, model_name: str, version: str):
        """Downloads a model given the language, name, and version.

        Args:
            language (str): language of the model, e.g. 'nl'
            model_name (str): name of the model, e.g. 'spacy'
            version (str): version of the model, e.g. '5.1'

        Returns:
            Path: the local path to the downloaded model (directory or file depending on the model type)
        """
        available_models = [
            x
            for x in cls._available_models
            if x.language == language and x.name == model_name and x.version == version
        ]

        if available_models:
            model = available_models[0]
            access_token = cls.__authenticate()
            url = cls._download_file_url.replace("{container}", cls._container)
            url = url.replace("{filename}", model.filename)
            response = requests.get(url, auth=cls.BearerAuth(access_token))

            if response.status_code == 200:
                if model.unzip:
                    dir = Path(Path.cwd(), "models", model.language, model.name)
                    dir.mkdir(parents=True, exist_ok=True)

                    zf = ZipFile(io.BytesIO(response.content), "r")
                    model_dir_zip = zf.namelist()[0]

                    zf.extractall(dir)

                    model.path = Path(dir, model_dir_zip)
                    cls._downloaded_models.append(model)

                    logger.info(f"Extracted model to: {model.path}")

                    return model.path
                else:
                    # Specify path to save
                    dir = Path(Path.cwd(), "models", model.language, model.name)
                    dir.mkdir(parents=True, exist_ok=True)
                    path = Path(dir, model.filename)

                    with open(path, "wb") as f:
                        f.write(response.content)

                    model.path = path
                    cls._downloaded_models.append(model)

                    logger.info(f"Saved model to: {model.path}")

                    return model.path

        return None

    @classmethod
    def download_latest_model(cls, language: str, model_name: str):
        """Download the latest available model for the given language and model name

        Args:
            language (str): language of the model, e.g. 'nl'
            model_name (str): name of the model, e.g. 'spacy'

        Returns:
            Path: the local path to the downloaded model (directory or file depending on the model type)
        """
        available_versions = [
            x.version
            for x in cls._available_models
            if x.language == language and x.name == model_name
        ]

        sorted_versions = natsorted(available_versions, reverse=True)
        if sorted_versions:
            latest_version = sorted_versions[0]

            path = cls.download_model(language, model_name, latest_version)
            if path:
                return path

        return None

    @classmethod
    def get_model(cls, language: str, model_name: str, version: str):
        downloaded_models = [
            x
            for x in cls._downloaded_models
            if x.language == language and x.name == model_name and x.version == version
        ]

        if downloaded_models:
            model = downloaded_models[0]
            if model.path:
                return model.path
            else:
                raise Exception("Path of downloaded model not set properly")
        else:
            cls.update_available_models()
            available_models = [
                x
                for x in cls._available_models
                if x.language == language
                and x.name == model_name
                and x.version == version
            ]

            if available_models:
                raise Exception(
                    f"Model {available_models[0].filename} is available, but not downloaded."
                )
            else:
                raise Exception("Model does not exist.")

    @classmethod
    def update_available_models(cls):
        """Updates the list of models available to download."""

        access_token = cls.__authenticate()
        files = cls.__get_files(access_token)

        for f in files:
            l = f.split("_")
            if len(l) < 4:
                continue

            language = l[0]
            model_name = l[1]
            version = l[2]
            extension = l[3]
            if extension == ".zip":
                unzip = True
            else:
                unzip = False

            if all([language, model_name, version]):
                model = PandoraModel(
                    language=language,
                    name=model_name,
                    version=version,
                    unzip=unzip,
                    filename=f,
                )
                if model not in cls._available_models:
                    cls._available_models.append(model)
            else:
                continue
