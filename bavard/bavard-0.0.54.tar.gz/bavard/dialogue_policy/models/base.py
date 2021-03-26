import datetime
import typing as t
from abc import abstractmethod

import tensorflow as tf
from bavard_ml_common.types.conversations.conversation import ConversationDataset, Conversation
from bavard_ml_common.types.ml import StrPredWithConf

from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, classification_report
from bavard_ml_common.mlops.serialization import Persistent
from bavard_ml_common.ml.utils import aggregate_dicts

from bavard.common.model_base import TFTunable


class BaseDPModel(TFTunable, Persistent):
    """
    Allows an inheriting dialogue policy base model to automatically
    inherit serialization and evaluation functionality. Also ensures the
    model has the correct fit and predict API (if the abstract methods are
    implemented in the way requested.)
    """

    @abstractmethod
    def fit(self, data: ConversationDataset) -> None:
        pass

    @abstractmethod
    def predict(self, conversations: t.List[Conversation]) -> t.List[t.List[StrPredWithConf]]:
        """
        Should take in raw conversations and for each one output a probability
        distribution over the possible next agent actions to take, conditioned on
        the conversation's state so far. The distribution should be sorted, so the
        highest probability action occurs first.
        """
        pass

    def evaluate(self, data: ConversationDataset, *, test_ratio: float = None, nfolds: int = None) -> dict:
        """
        Performs cross validation to evaluate the model's training set performance
        and generalizable performance on `agent`.

        Parameters
        ----------
        data : ConversationDataset
            The conversations to train and evaluate on.
        test_ratio : float
            If provided, a basic stratified train/test split will be used.
        nfolds : int
            If provided, stratified k-fold cross validation will be conducted with `k==nfolds`.
        """
        if test_ratio is not None and nfolds is not None:
            raise ValueError("please supply either test_ratio or nfolds, but not both")

        if test_ratio is not None:
            return self._evaluate_train_test(data, test_ratio)
        elif nfolds is not None:
            return self._evaluate_kfold_cv(data, nfolds)
        else:
            raise ValueError("please supply either test_ratio or nfolds")

    def _evaluate_train_test(self, data: ConversationDataset, test_ratio: float) -> dict:
        # Evaluate the model on a basic train/test split.
        train_data, test_data = data.split(test_ratio)
        return self._evaluate(train_data, test_data)

    def _evaluate_kfold_cv(self, data: ConversationDataset, nfolds: int) -> dict:
        # Evaluate the model using k-fold cross validation.
        results = []
        for train_data, test_data in data.cv(nfolds):
            results.append(self._evaluate(train_data, test_data))

        # Now average the k performance results.
        performance = aggregate_dicts(results, "mean")
        return performance

    def _evaluate(self, train_data: ConversationDataset, test_data: ConversationDataset) -> dict:
        self.fit(train_data)
        scores = {}
        scores.update({f"train_{k}": v for k, v in self.score(train_data).items()})
        scores.update({f"test_{k}": v for k, v in self.score(test_data).items()})
        return scores

    def score(self, data: ConversationDataset) -> dict:
        convs, next_actions = data.make_validation_pairs()
        # Take the highest confidence prediction for each conversation for calculating the metrics.
        predicted_actions = [preds[0].value for preds in self.predict(convs)]
        return {
            "f1_macro": f1_score(next_actions, predicted_actions, average="macro"),
            "accuracy": accuracy_score(next_actions, predicted_actions),
            "classification_report": classification_report(next_actions, predicted_actions, output_dict=True),
            "confusion_matrix": confusion_matrix(next_actions, predicted_actions)
        }

    @classmethod
    def tune(
        cls,
        data: ConversationDataset,
        *,
        val_ratio: float = None,
        nfolds: int = None,
        **tune_args
    ):
        """
        Performs hyperparameter optimization of the model over `agent`. Optimizes
        (maximizes) the validation set f1 macro score.

        Parameters
        ----------
        data : ConversationDataset
            The conversations to optimize over.
        val_ratio : float, optional
            The % of the agent's training conversations to use for the
            validation set (randomly selected).
        nfolds : int, optional
            The number of folds to do in k-fold cross validation.
        **tune_args : kwargs, optional
            Any other arguments to pass to the underlying tune method.
        """
        super().tune(
            objective_name="test_f1_macro",
            objective=lambda model: model.evaluate(data, test_ratio=val_ratio, nfolds=nfolds),
            mode="max",
            **tune_args
        )

    def get_tensorboard_cb(self) -> tf.keras.callbacks.TensorBoard:
        log_dir = f"logs/{self.__class__.__name__}/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return tf.keras.callbacks.TensorBoard(log_dir=log_dir)
