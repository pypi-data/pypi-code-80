import logging

from .fairness import Fairness

logger = logging.getLogger(__name__)


class RegressionFairness(Fairness):
    def analyze_fairness(self):
        pass

