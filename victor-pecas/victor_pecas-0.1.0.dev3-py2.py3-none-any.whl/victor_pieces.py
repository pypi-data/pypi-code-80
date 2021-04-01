import logging
import pickle
import sys

import numpy as np  # noqa: F401
from pre_processing import CorpusHandler as ch

from .tfidf_vectorizer import TfidfTransformer2, TfidfVectorizer_Gpam

logger = logging.getLogger(__name__)


class VictorPieces:
    def __init__(self, model_path, tfidf_path):

        setattr(sys.modules["__main__"], "TfidfTransformer2", TfidfTransformer2)
        setattr(sys.modules["__main__"], "TfidfVectorizer_Gpam", TfidfVectorizer_Gpam)

        self.model = self.load_model(model_path)
        self.tfidf = self.load_tfidf(tfidf_path)

    def predict(self, data):

        logger.info("Make prediction")

        logger.debug("Parsing data")
        data = self.parse_data(data)
        logger.debug("Data parsed")

        logger.debug("Getting output from model")
        output = self.model_output(data)
        logger.debug("Output taked successfully")

        logger.info("Finish prediction")

        return output

    def load_tfidf(self, tfidf_path):

        tfidf = pickle.load(open(tfidf_path, "rb"))
        return tfidf

    def load_model(self, model_path):

        model = pickle.load(open(model_path, "rb"))
        return model

    def parse_data(self, data):

        parsed_data = ch.preprocess(
            data, disabled=["spellchecker", "to_st_named_entities", "lemmatize"]
        )
        parsed_data = " ".join(parsed_data)

        vectorized_data = self.tfidf.transform([parsed_data])

        return vectorized_data

    def model_output(self, data):

        output = self.model.predict(data)

        return output
