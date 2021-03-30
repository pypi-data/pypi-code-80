# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import sys
import uuid
from enum import Enum
from pathlib import Path

import apistar
import gnupg
import yaml
from apistar.exceptions import ErrorResponse
from peewee import IntegrityError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex import ArkindexClient, options_from_env
from arkindex_worker import logger
from arkindex_worker.cache import (
    CachedElement,
    CachedImage,
    CachedTranscription,
    create_tables,
    init_cache_db,
    merge_parents_cache,
)
from arkindex_worker.models import Element
from arkindex_worker.reporting import Reporter

MANUAL_SLUG = "manual"


def _is_500_error(exc):
    """
    Check if an Arkindex API error is a 50x
    This is used to retry most API calls implemented here
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


class BaseWorker(object):
    def __init__(self, description="Arkindex Base Worker", use_cache=False):
        self.parser = argparse.ArgumentParser(description=description)

        # Setup workdir either in Ponos environment or on host's home
        if os.environ.get("PONOS_DATA"):
            self.work_dir = os.path.join(os.environ["PONOS_DATA"], "current")
        else:
            # We use the official XDG convention to store file for developers
            # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
            xdg_data_home = os.environ.get(
                "XDG_DATA_HOME", os.path.expanduser("~/.local/share")
            )
            self.work_dir = os.path.join(xdg_data_home, "arkindex")
            os.makedirs(self.work_dir, exist_ok=True)

        self.worker_version_id = os.environ.get("WORKER_VERSION_ID")
        if not self.worker_version_id:
            logger.warning(
                "Missing WORKER_VERSION_ID environment variable, worker is in read-only mode"
            )

        logger.info(f"Worker will use {self.work_dir} as working directory")

        self.use_cache = use_cache
        if self.use_cache is True:
            if os.environ.get("TASK_ID"):
                cache_dir = f"/data/{os.environ.get('TASK_ID')}"
                assert os.path.isdir(cache_dir), f"Missing task cache in {cache_dir}"
                self.cache_path = os.path.join(cache_dir, "db.sqlite")
            else:
                self.cache_path = os.path.join(os.getcwd(), "db.sqlite")

            init_cache_db(self.cache_path)
            create_tables()
        else:
            logger.debug("Cache is disabled")

    @property
    def is_read_only(self):
        """Worker cannot publish anything without a worker version ID"""
        return self.worker_version_id is None

    def configure(self):
        """
        Configure worker using cli args and environment variables
        """
        self.parser.add_argument(
            "-c",
            "--config",
            help="Alternative configuration file when running without a Worker Version ID",
            type=open,
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            help="Display more information on events and errors",
            action="store_true",
            default=False,
        )

        # Call potential extra arguments
        self.add_arguments()

        # CLI args are stored on the instance so that implementations can access them
        self.args = self.parser.parse_args()

        # Setup logging level
        if self.args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

        # Build Arkindex API client from environment variables
        self.api_client = ArkindexClient(**options_from_env())
        logger.debug(f"Setup Arkindex API client on {self.api_client.document.url}")

        # Load features available on backend, and check authentication
        user = self.request("RetrieveUser")
        logger.debug(f"Connected as {user['display_name']} - {user['email']}")
        self.features = user["features"]

        if self.worker_version_id:
            # Retrieve initial configuration from API
            worker_version = self.request(
                "RetrieveWorkerVersion", id=self.worker_version_id
            )
            logger.info(
                f"Loaded worker {worker_version['worker']['name']} revision {worker_version['revision']['hash'][0:7]} from API"
            )
            self.config = worker_version["configuration"]["configuration"]
            required_secrets = worker_version["configuration"].get("secrets", [])
        elif self.args.config:
            # Load config from YAML file
            self.config = yaml.safe_load(self.args.config)
            required_secrets = self.config.get("secrets", [])
            logger.info(
                f"Running with local configuration from {self.args.config.name}"
            )
        else:
            self.config = {}
            required_secrets = []
            logger.warning("Running without any extra configuration")

        # Load all required secrets
        self.secrets = {name: self.load_secret(name) for name in required_secrets}

        # Merging parents caches (if there are any) in the current task local cache
        task_id = os.environ.get("TASK_ID")
        if self.use_cache and task_id is not None:
            task = self.request("RetrieveTaskFromAgent", id=task_id)
            merge_parents_cache(
                task["parents"],
                self.cache_path,
                data_dir=os.environ.get("PONOS_DATA_DIR", "/data"),
                chunk=os.environ.get("ARKINDEX_TASK_CHUNK"),
            )

    def load_secret(self, name):
        """Load all secrets described in the worker configuration"""
        secret = None

        # Load from the backend
        try:
            resp = self.request("RetrieveSecret", name=name)
            secret = resp["content"]
            logging.info(f"Loaded API secret {name}")
        except ErrorResponse as e:
            logger.warning(f"Secret {name} not available: {e.content}")

        # Load from local developer storage
        base_dir = Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser()
        path = base_dir / "arkindex" / "secrets" / name
        if path.exists():
            logging.debug(f"Loading local secret from {path}")

            try:
                gpg = gnupg.GPG()
                decrypted = gpg.decrypt_file(open(path, "rb"))
                assert (
                    decrypted.ok
                ), f"GPG error: {decrypted.status} - {decrypted.stderr}"
                secret = decrypted.data.decode("utf-8")
                logging.info(f"Loaded local secret {name}")
            except Exception as e:
                logger.error(f"Local secret {name} is not available as {path}: {e}")

        if secret is None:
            raise Exception(f"Secret {name} is not available on the API nor locally")

        # Parse secret payload, according to its extension
        _, ext = os.path.splitext(os.path.basename(name))
        try:
            ext = ext.lower()
            if ext == ".json":
                return json.loads(secret)
            elif ext in (".yaml", ".yml"):
                return yaml.safe_load(secret)
        except Exception as e:
            logger.error(f"Failed to parse secret {name}: {e}")

        # By default give raw secret payload
        return secret

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(self, *args, **kwargs):
        """
        Proxy all Arkindex API requests with a retry mechanism
        in case of 50X errors
        The same API call will be retried 5 times, with an exponential sleep time
        going through 3, 4, 8 and 16 seconds of wait between call.
        If the 5th call still gives a 50x, the exception is re-raised
        and the caller should catch it
        Log messages are displayed before sleeping (when at least one exception occurred)
        """
        return self.api_client.request(*args, **kwargs)

    def add_arguments(self):
        """Override this method to add argparse argument to this worker"""

    def run(self):
        """Override this method to implement your own process"""


class EntityType(Enum):
    Person = "person"
    Location = "location"
    Subject = "subject"
    Organization = "organization"
    Misc = "misc"
    Number = "number"
    Date = "date"


class MetaType(Enum):
    Text = "text"
    HTML = "html"
    Date = "date"
    Location = "location"
    # Element's original structure reference (intended to be indexed)
    Reference = "reference"


class ActivityState(Enum):
    Queued = "queued"
    Started = "started"
    Processed = "processed"
    Error = "error"


class ElementsWorker(BaseWorker):
    def __init__(self, description="Arkindex Elements Worker", use_cache=False):
        super().__init__(description, use_cache)

        # Add report concerning elements
        self.report = Reporter("unknown worker")

        # Add mandatory argument to process elements
        self.parser.add_argument(
            "--elements-list",
            help="JSON elements list to use",
            type=open,
            default=os.environ.get("TASK_ELEMENTS"),
        )
        self.parser.add_argument(
            "--element",
            type=uuid.UUID,
            nargs="+",
            help="One or more Arkindex element ID",
        )
        self.classes = {}

        self._worker_version_cache = {}

    def list_elements(self):
        assert not (
            self.args.elements_list and self.args.element
        ), "elements-list and element CLI args shouldn't be both set"
        out = []

        # Process elements from JSON file
        if self.args.elements_list:
            data = json.load(self.args.elements_list)
            assert isinstance(data, list), "Elements list must be a list"
            assert len(data), "No elements in elements list"
            out += list(filter(None, [element.get("id") for element in data]))
        # Add any extra element from CLI
        elif self.args.element:
            out += self.args.element

        return out

    def run(self):
        """
        Process every elements from the provided list
        """
        self.configure()

        # List all elements either from JSON file
        # or direct list of elements on CLI
        elements = self.list_elements()
        if not elements:
            logger.warning("No elements to process, stopping.")
            sys.exit(1)

        # Process every element
        count = len(elements)
        failed = 0
        for i, element_id in enumerate(elements, start=1):
            try:
                # Load element using Arkindex API
                element = Element(**self.request("RetrieveElement", id=element_id))
                logger.info(f"Processing {element} ({i}/{count})")

                # Report start of process, run process, then report end of process
                self.update_activity(element, ActivityState.Started)
                self.process_element(element)
                self.update_activity(element, ActivityState.Processed)
            except ErrorResponse as e:
                failed += 1
                logger.warning(
                    f"An API error occurred while processing element {element_id}: {e.title} - {e.content}",
                    exc_info=e if self.args.verbose else None,
                )
                self.update_activity(element, ActivityState.Error)
                self.report.error(element_id, e)
            except Exception as e:
                failed += 1
                logger.warning(
                    f"Failed running worker on element {element_id}: {e}",
                    exc_info=e if self.args.verbose else None,
                )
                self.update_activity(element, ActivityState.Error)
                self.report.error(element_id, e)

        # Save report as local artifact
        self.report.save(os.path.join(self.work_dir, "ml_report.json"))

        if failed:
            logger.error(
                "Ran on {} elements: {} completed, {} failed".format(
                    count, count - failed, failed
                )
            )
            if failed >= count:  # Everything failed!
                sys.exit(1)

    def process_element(self, element):
        """Override this method to analyze an Arkindex element from the provided list"""

    def load_corpus_classes(self, corpus_id):
        """
        Load ML classes for the given corpus ID
        """
        corpus_classes = self.api_client.paginate(
            "ListCorpusMLClasses",
            id=corpus_id,
        )
        self.classes[corpus_id] = {
            ml_class["name"]: ml_class["id"] for ml_class in corpus_classes
        }
        logger.info(f"Loaded {len(self.classes[corpus_id])} ML classes")

    def get_ml_class_id(self, corpus_id, ml_class):
        """
        Return the ID corresponding to the given class name on a specific corpus
        This method will automatically create missing classes
        """
        if not self.classes.get(corpus_id):
            self.load_corpus_classes(corpus_id)

        ml_class_id = self.classes[corpus_id].get(ml_class)
        if ml_class_id is None:
            logger.info(f"Creating ML class {ml_class} on corpus {corpus_id}")
            try:
                response = self.request(
                    "CreateMLClass", id=corpus_id, body={"name": ml_class}
                )
                ml_class_id = self.classes[corpus_id][ml_class] = response["id"]
                logger.debug(f"Created ML class {response['id']}")
            except apistar.exceptions.ErrorResponse as e:
                # Only reload for 400 errors
                if e.status_code != 400:
                    raise

                # Reload and make sure we have the class
                logger.info(
                    f"Reloading corpus classes to see if {ml_class} already exists"
                )
                self.load_corpus_classes(corpus_id)
                assert (
                    ml_class in self.classes[corpus_id]
                ), "Missing class {ml_class} even after reloading"
                ml_class_id = self.classes[corpus_id][ml_class]

        return ml_class_id

    def create_sub_element(self, element, type, name, polygon):
        """
        Create a child element on the given element through API
        Return the ID of the created sub element
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert type and isinstance(
            type, str
        ), "type shouldn't be null and should be of type str"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert polygon and isinstance(
            polygon, list
        ), "polygon shouldn't be null and should be of type list"
        assert len(polygon) >= 3, "polygon should have at least three points"
        assert all(
            isinstance(point, list) and len(point) == 2 for point in polygon
        ), "polygon points should be lists of two items"
        assert all(
            isinstance(coord, (int, float)) for point in polygon for coord in point
        ), "polygon points should be lists of two numbers"
        if self.is_read_only:
            logger.warning("Cannot create element as this worker is in read-only mode")
            return

        sub_element = self.request(
            "CreateElement",
            body={
                "type": type,
                "name": name,
                "image": element.zone.image.id,
                "corpus": element.corpus.id,
                "polygon": polygon,
                "parent": element.id,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_element(element.id, type)

        return sub_element["id"]

    def create_elements(self, parent, elements):
        """
        Create children elements on the given element through API
        Return the IDs of created elements
        """
        if isinstance(parent, Element):
            assert parent.get(
                "zone"
            ), "create_elements cannot be used on parents without zones"
        elif isinstance(parent, CachedElement):
            assert (
                parent.image_id
            ), "create_elements cannot be used on parents without images"
        else:
            raise TypeError(
                "Parent element should be an Element or CachedElement instance"
            )

        assert elements and isinstance(
            elements, list
        ), "elements shouldn't be null and should be of type list"

        for index, element in enumerate(elements):
            assert isinstance(
                element, dict
            ), f"Element at index {index} in elements: Should be of type dict"

            name = element.get("name")
            assert name and isinstance(
                name, str
            ), f"Element at index {index} in elements: name shouldn't be null and should be of type str"

            type = element.get("type")
            assert type and isinstance(
                type, str
            ), f"Element at index {index} in elements: type shouldn't be null and should be of type str"

            polygon = element.get("polygon")
            assert polygon and isinstance(
                polygon, list
            ), f"Element at index {index} in elements: polygon shouldn't be null and should be of type list"
            assert (
                len(polygon) >= 3
            ), f"Element at index {index} in elements: polygon should have at least three points"
            assert all(
                isinstance(point, list) and len(point) == 2 for point in polygon
            ), f"Element at index {index} in elements: polygon points should be lists of two items"
            assert all(
                isinstance(coord, (int, float)) for point in polygon for coord in point
            ), f"Element at index {index} in elements: polygon points should be lists of two numbers"

        if self.is_read_only:
            logger.warning("Cannot create elements as this worker is in read-only mode")
            return

        created_ids = self.request(
            "CreateElements",
            id=parent.id,
            body={
                "worker_version": self.worker_version_id,
                "elements": elements,
            },
        )

        for element in elements:
            self.report.add_element(parent.id, element["type"])

        if self.use_cache:
            # Create the image as needed and handle both an Element and a CachedElement
            if isinstance(parent, CachedElement):
                image_id = parent.image_id
            else:
                image_id = parent.zone.image.id
                CachedImage.get_or_create(
                    id=parent.zone.image.id,
                    defaults={
                        "width": parent.zone.image.width,
                        "height": parent.zone.image.height,
                        "url": parent.zone.image.url,
                    },
                )

            # Store elements in local cache
            try:
                to_insert = [
                    {
                        "id": created_ids[idx]["id"],
                        "parent_id": parent.id,
                        "type": element["type"],
                        "image_id": image_id,
                        "polygon": element["polygon"],
                        "worker_version_id": self.worker_version_id,
                    }
                    for idx, element in enumerate(elements)
                ]
                CachedElement.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(f"Couldn't save created elements in local cache: {e}")

        return created_ids

    def create_transcription(self, element, text, score):
        """
        Create a transcription on the given element through the API.
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        assert text and isinstance(
            text, str
        ), "text shouldn't be null and should be of type str"

        assert (
            isinstance(score, float) and 0 <= score <= 1
        ), "score shouldn't be null and should be a float in [0..1] range"

        if self.is_read_only:
            logger.warning(
                "Cannot create transcription as this worker is in read-only mode"
            )
            return

        created = self.request(
            "CreateTranscription",
            id=element.id,
            body={
                "text": text,
                "worker_version": self.worker_version_id,
                "score": score,
            },
        )

        self.report.add_transcription(element.id)

        if self.use_cache:
            # Store transcription in local cache
            try:
                to_insert = [
                    {
                        "id": created["id"],
                        "element_id": element.id,
                        "text": created["text"],
                        "confidence": created["confidence"],
                        "worker_version_id": self.worker_version_id,
                    }
                ]
                CachedTranscription.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcription in local cache: {e}"
                )

    def create_transcriptions(self, transcriptions):
        """
        Create multiple transcriptions at once on existing elements through the API.
        """

        assert transcriptions and isinstance(
            transcriptions, list
        ), "transcriptions shouldn't be null and should be of type list"

        for index, transcription in enumerate(transcriptions):
            element_id = transcription.get("element_id")
            assert element_id and isinstance(
                element_id, str
            ), f"Transcription at index {index} in transcriptions: element_id shouldn't be null and should be of type str"

            text = transcription.get("text")
            assert text and isinstance(
                text, str
            ), f"Transcription at index {index} in transcriptions: text shouldn't be null and should be of type str"

            score = transcription.get("score")
            assert (
                score is not None and isinstance(score, float) and 0 <= score <= 1
            ), f"Transcription at index {index} in transcriptions: score shouldn't be null and should be a float in [0..1] range"

        created_trs = self.request(
            "CreateTranscriptions",
            body={
                "worker_version": self.worker_version_id,
                "transcriptions": transcriptions,
            },
        )["transcriptions"]

        for created_tr in created_trs:
            self.report.add_transcription(created_tr["element_id"])

        if self.use_cache:
            # Store transcriptions in local cache
            try:
                to_insert = [
                    {
                        "id": created_tr["id"],
                        "element_id": created_tr["element_id"],
                        "text": created_tr["text"],
                        "confidence": created_tr["confidence"],
                        "worker_version_id": self.worker_version_id,
                    }
                    for created_tr in created_trs
                ]
                CachedTranscription.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcriptions in local cache: {e}"
                )

    def create_classification(
        self, element, ml_class, confidence, high_confidence=False
    ):
        """
        Create a classification on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert ml_class and isinstance(
            ml_class, str
        ), "ml_class shouldn't be null and should be of type str"
        assert (
            isinstance(confidence, float) and 0 <= confidence <= 1
        ), "confidence shouldn't be null and should be a float in [0..1] range"
        assert isinstance(
            high_confidence, bool
        ), "high_confidence shouldn't be null and should be of type bool"
        if self.is_read_only:
            logger.warning(
                "Cannot create classification as this worker is in read-only mode"
            )
            return

        try:
            self.request(
                "CreateClassification",
                body={
                    "element": element.id,
                    "ml_class": self.get_ml_class_id(element.corpus.id, ml_class),
                    "worker_version": self.worker_version_id,
                    "confidence": confidence,
                    "high_confidence": high_confidence,
                },
            )
        except ErrorResponse as e:

            # Detect already existing classification
            if (
                e.status_code == 400
                and "non_field_errors" in e.content
                and "The fields element, worker_version, ml_class must make a unique set."
                in e.content["non_field_errors"]
            ):
                logger.warning(
                    f"This worker version has already set {ml_class} on element {element.id}"
                )
                return

            # Propagate any other API error
            raise

        self.report.add_classification(element.id, ml_class)

    def create_entity(self, element, name, type, corpus, metas=None, validated=None):
        """
        Create an entity on the given corpus through API
        Return the ID of the created entity
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert type and isinstance(
            type, EntityType
        ), "type shouldn't be null and should be of type EntityType"
        assert corpus and isinstance(
            corpus, str
        ), "corpus shouldn't be null and should be of type str"
        if metas:
            assert isinstance(metas, dict), "metas should be of type dict"
        if validated is not None:
            assert isinstance(validated, bool), "validated should be of type bool"
        if self.is_read_only:
            logger.warning("Cannot create entity as this worker is in read-only mode")
            return

        entity = self.request(
            "CreateEntity",
            body={
                "name": name,
                "type": type.value,
                "metas": metas,
                "validated": validated,
                "corpus": corpus,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_entity(element.id, entity["id"], type.value, name)

        return entity["id"]

    def create_element_transcriptions(self, element, sub_element_type, transcriptions):
        """
        Create multiple sub elements with their transcriptions on the given element through API
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        assert sub_element_type and isinstance(
            sub_element_type, str
        ), "sub_element_type shouldn't be null and should be of type str"
        assert transcriptions and isinstance(
            transcriptions, list
        ), "transcriptions shouldn't be null and should be of type list"

        for index, transcription in enumerate(transcriptions):
            text = transcription.get("text")
            assert text and isinstance(
                text, str
            ), f"Transcription at index {index} in transcriptions: text shouldn't be null and should be of type str"

            score = transcription.get("score")
            assert (
                score is not None and isinstance(score, float) and 0 <= score <= 1
            ), f"Transcription at index {index} in transcriptions: score shouldn't be null and should be a float in [0..1] range"

            polygon = transcription.get("polygon")
            assert polygon and isinstance(
                polygon, list
            ), f"Transcription at index {index} in transcriptions: polygon shouldn't be null and should be of type list"
            assert (
                len(polygon) >= 3
            ), f"Transcription at index {index} in transcriptions: polygon should have at least three points"
            assert all(
                isinstance(point, list) and len(point) == 2 for point in polygon
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two items"
            assert all(
                isinstance(coord, (int, float)) for point in polygon for coord in point
            ), f"Transcription at index {index} in transcriptions: polygon points should be lists of two numbers"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcriptions as this worker is in read-only mode"
            )
            return

        annotations = self.request(
            "CreateElementTranscriptions",
            id=element.id,
            body={
                "element_type": sub_element_type,
                "worker_version": self.worker_version_id,
                "transcriptions": transcriptions,
                "return_elements": True,
            },
        )

        for annotation in annotations:
            if annotation["created"]:
                logger.debug(
                    f"A sub_element of {element.id} with type {sub_element_type} was created during transcriptions bulk creation"
                )
                self.report.add_element(element.id, sub_element_type)
            self.report.add_transcription(annotation["element_id"])

        if self.use_cache:
            # Store transcriptions and their associated element (if created) in local cache
            created_ids = set()
            elements_to_insert = []
            transcriptions_to_insert = []
            for index, annotation in enumerate(annotations):
                transcription = transcriptions[index]

                if annotation["element_id"] not in created_ids:
                    # Even if the API says the element already existed in the DB,
                    # we need to check if it is available in the local cache.
                    # Peewee does not have support for SQLite's INSERT OR IGNORE,
                    # so we do the check here, element by element.
                    try:
                        CachedElement.get_by_id(annotation["element_id"])
                    except CachedElement.DoesNotExist:
                        elements_to_insert.append(
                            {
                                "id": annotation["element_id"],
                                "parent_id": element.id,
                                "type": sub_element_type,
                                "image_id": element.image_id,
                                "polygon": transcription["polygon"],
                                "worker_version_id": self.worker_version_id,
                            }
                        )

                    created_ids.add(annotation["element_id"])

                transcriptions_to_insert.append(
                    {
                        "id": annotation["id"],
                        "element_id": annotation["element_id"],
                        "text": transcription["text"],
                        "confidence": transcription["score"],
                        "worker_version_id": self.worker_version_id,
                    }
                )

            try:
                CachedElement.insert_many(elements_to_insert).execute()
                CachedTranscription.insert_many(transcriptions_to_insert).execute()
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcriptions in local cache: {e}"
                )

        return annotations

    def create_metadata(self, element, type, name, value, entity=None):
        """
        Create a metadata on the given element through API
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert type and isinstance(
            type, MetaType
        ), "type shouldn't be null and should be of type MetaType"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert value and isinstance(
            value, str
        ), "value shouldn't be null and should be of type str"
        if entity:
            assert isinstance(entity, str), "entity should be of type str"
        if self.is_read_only:
            logger.warning("Cannot create metadata as this worker is in read-only mode")
            return

        metadata = self.request(
            "CreateMetaData",
            id=element.id,
            body={
                "type": type.value,
                "name": name,
                "value": value,
                "entity": entity,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_metadata(element.id, metadata["id"], type.value, name)

        return metadata["id"]

    def get_worker_version(self, worker_version_id: str) -> dict:
        """
        Get worker version from cache if possible, otherwise make API request
        """
        if worker_version_id in self._worker_version_cache:
            return self._worker_version_cache[worker_version_id]

        worker_version = self.request("RetrieveWorkerVersion", id=worker_version_id)
        self._worker_version_cache[worker_version_id] = worker_version

        return worker_version

    def get_worker_version_slug(self, worker_version_id: str) -> str:
        """
        Get worker version slug from cache if possible, otherwise make API request

        Should use `get_ml_result_slug` instead of using this method directly
        """
        worker_version = self.get_worker_version(worker_version_id)
        return worker_version["worker"]["slug"]

    def get_ml_result_slug(self, ml_result) -> str:
        """
        Helper function to get the slug from element, classification or transcription

        Can handle old and new (source vs worker_version)

        :type ml_result: Element or classification or transcription
        """
        if (
            "source" in ml_result
            and ml_result["source"]
            and ml_result["source"]["slug"]
        ):
            return ml_result["source"]["slug"]
        elif "worker_version" in ml_result and ml_result["worker_version"]:
            return self.get_worker_version_slug(ml_result["worker_version"])
        # transcriptions have worker_version_id but elements have worker_version
        elif "worker_version_id" in ml_result and ml_result["worker_version_id"]:
            return self.get_worker_version_slug(ml_result["worker_version_id"])
        elif "worker_version" in ml_result and ml_result["worker_version"] is None:
            return MANUAL_SLUG
        elif (
            "worker_version_id" in ml_result and ml_result["worker_version_id"] is None
        ):
            return MANUAL_SLUG
        else:
            raise ValueError(f"Unable to get slug from: {ml_result}")

    def list_transcriptions(
        self, element, element_type=None, recursive=None, worker_version=None
    ):
        """
        List transcriptions on an element
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        query_params = {}
        if element_type:
            assert isinstance(element_type, str), "element_type should be of type str"
            query_params["element_type"] = element_type
        if recursive is not None:
            assert isinstance(recursive, bool), "recursive should be of type bool"
            query_params["recursive"] = recursive
        if worker_version:
            assert isinstance(
                worker_version, str
            ), "worker_version should be of type str"
            query_params["worker_version"] = worker_version

        if self.use_cache and recursive is None:
            # Checking that we only received query_params handled by the cache
            assert set(query_params.keys()) <= {
                "worker_version",
            }, "When using the local cache, you can only filter by 'worker_version'"

            transcriptions = CachedTranscription.select().where(
                CachedTranscription.element_id == element.id
            )
            if worker_version:
                transcriptions = transcriptions.where(
                    CachedTranscription.worker_version_id == worker_version
                )
        else:
            if self.use_cache:
                logger.warning(
                    "'recursive' filter was set, results will be retrieved from the API since the local cache doesn't handle this filter."
                )
            transcriptions = self.api_client.paginate(
                "ListTranscriptions", id=element.id, **query_params
            )

        return transcriptions

    def list_element_children(
        self,
        element,
        best_class=None,
        folder=None,
        name=None,
        recursive=None,
        type=None,
        with_best_classes=None,
        with_corpus=None,
        with_has_children=None,
        with_zone=None,
        worker_version=None,
    ):
        """
        List children of an element
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        query_params = {}
        if best_class is not None:
            assert isinstance(best_class, str) or isinstance(
                best_class, bool
            ), "best_class should be of type str or bool"
            query_params["best_class"] = best_class
        if folder is not None:
            assert isinstance(folder, bool), "folder should be of type bool"
            query_params["folder"] = folder
        if name:
            assert isinstance(name, str), "name should be of type str"
            query_params["name"] = name
        if recursive is not None:
            assert isinstance(recursive, bool), "recursive should be of type bool"
            query_params["recursive"] = recursive
        if type:
            assert isinstance(type, str), "type should be of type str"
            query_params["type"] = type
        if with_best_classes is not None:
            assert isinstance(
                with_best_classes, bool
            ), "with_best_classes should be of type bool"
            query_params["with_best_classes"] = with_best_classes
        if with_corpus is not None:
            assert isinstance(with_corpus, bool), "with_corpus should be of type bool"
            query_params["with_corpus"] = with_corpus
        if with_has_children is not None:
            assert isinstance(
                with_has_children, bool
            ), "with_has_children should be of type bool"
            query_params["with_has_children"] = with_has_children
        if with_zone is not None:
            assert isinstance(with_zone, bool), "with_zone should be of type bool"
            query_params["with_zone"] = with_zone
        if worker_version:
            assert isinstance(
                worker_version, str
            ), "worker_version should be of type str"
            query_params["worker_version"] = worker_version

        if self.use_cache:
            # Checking that we only received query_params handled by the cache
            assert set(query_params.keys()) <= {
                "type",
                "worker_version",
            }, "When using the local cache, you can only filter by 'type' and/or 'worker_version'"

            query = CachedElement.select().where(CachedElement.parent_id == element.id)
            if type:
                query = query.where(CachedElement.type == type)
            if worker_version:
                query = query.where(CachedElement.worker_version_id == worker_version)

            return query
        else:
            children = self.api_client.paginate(
                "ListElementChildren", id=element.id, **query_params
            )

        return children

    def update_activity(self, element, state):
        """
        Update worker activity for this element
        This method should not raise a runtime exception, but simply warn users
        """
        assert element and isinstance(
            element, Element
        ), "element shouldn't be null and should be of type Element"
        assert isinstance(state, ActivityState), "state should be an ActivityState"

        if not self.features.get("workers_activity"):
            logger.debug("Skipping Worker activity update as it's disabled on backend")
            return

        if self.is_read_only:
            logger.warning("Cannot update activity as this worker is in read-only mode")
            return

        try:
            out = self.request(
                "UpdateWorkerActivity",
                id=self.worker_version_id,
                body={
                    "element_id": element.id,
                    "state": state.value,
                },
            )
            logger.debug(f"Updated activity of element {element.id} to {state}")
            return out
        except ErrorResponse as e:
            logger.warning(
                f"Failed to update activity of element {element.id} to {state.value} due to an API error: {e.content}"
            )
        except Exception as e:
            logger.warning(
                f"Failed to update activity of element {element.id} to {state.value}: {e}"
            )
