import logging
from datetime import datetime
import typing as t
from time import time

import numpy as np
import tensorflow as tf
from bavard_ml_common.types.ml import StrPredWithConf

from bavard.config import logger
from tensorflow.keras.layers import Input, Dense, TimeDistributed, Lambda
from tensorflow.keras import Model
import tensorflow_probability as tfp
import uncertainty_metrics.tensorflow as um
from bavard_ml_common.mlops.serialization import Persistent, Serializer
from bavard_ml_common.ml.utils import aggregate_dicts
from bavard_ml_common.types.nlu import NLUExampleDataset
import kerastuner as kt

from bavard.common.layers import model_bodies
from bavard.common.model_base import TFTunable
from bavard.common.serialization import KerasSerializer
from bavard.nlu.data.preprocessor import NLUDataPreprocessor
from bavard.nlu.auto_setup import AutoSetup
from bavard.nlu.pydantics import NLUPredictions, NLUPrediction
from bavard.common.pretrained_bases import pretrained_bases

logging.getLogger().setLevel(logging.DEBUG)


class NLUModel(Persistent, TFTunable):

    serializer = Serializer(KerasSerializer())

    # Always predict on larger batches, for efficiency's sake,
    # since it doesn't affect the model's optimization.
    batch_size_predict = 64
    max_seq_len: int = 120

    def __init__(
        self,
        *,
        save_model_dir: t.Optional[str] = None,
        auto: bool = False,
        hidden_size: int = 323,
        dropout: float = 0.1235,
        l2_regularization: float = 1.069e-11,
        n_hidden_layers: int = 3,
        fine_tune_base: bool = True,
        learning_rate: float = 0.00004185,
        batch_size: int = 4,
        epochs: int = 15,
        body: str = "encoder",
        balance_intent: bool = True,
        pretrain_base_name: str = "distilbert-base-multilingual-cased"
    ):
        # Control parameters
        self.auto = auto
        self.save_model_dir = save_model_dir
        self._fitted = False

        # Hyperparameters
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.l2_regularization = l2_regularization
        self.n_hidden_layers = n_hidden_layers
        self.fine_tune_base = fine_tune_base
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.body = body
        self.balance_intent = balance_intent
        self.pretrain_base_name = pretrain_base_name
        self.preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len, lm_name=self.pretrain_base_name)

    @staticmethod
    def get_hp_spec(hp: kt.HyperParameters) -> t.Dict[str, kt.engine.hyperparameters.HyperParameter]:
        return {
            "hidden_size": hp.Int("hidden_size", 32, 512, default=256),
            "dropout": hp.Float("dropout", 0.0, 0.6, default=0.1),
            "l2_regularization": hp.Float("l2_regularization", 1e-12, 0.1, sampling="log"),
            "n_hidden_layers": hp.Int("n_hidden_layers", 1, 5),
            "fine_tune_base": hp.Boolean("fine_tune_base", default=True),
            "learning_rate": hp.Float("learning_rate", 1e-7, 0.1, sampling="log", default=5e-5),
            "epochs": hp.Int("epochs", 5, 200, step=5, default=15),
            "body": hp.Choice("body", list(model_bodies.keys())),
            "balance_intent": hp.Boolean("balance_intent", default=False),
            "batch_size": hp.Choice("batch_size", [2**2, 2**3, 2**4]),
            "pretrain_base_name": hp.Choice("pretrain_base_name", list(pretrained_bases.keys()))
        }

    def _build_and_compile_model(self) -> None:
        embedder = pretrained_bases[self.pretrain_base_name](self.fine_tune_base)

        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_mask', dtype=tf.int32)

        # The output of the pretrained base model.
        pooled_embedding, token_embeddings = embedder(in_id, in_mask)

        # A network for intent classification.

        intent_out = token_embeddings if self.body in {"lstm", "encoder"} else pooled_embedding
        intent_out = model_bodies[self.body](
            num_blocks=self.n_hidden_layers,
            units=self.hidden_size,
            dropout=self.dropout,
            l2=self.l2_regularization,
            return_sequences=False
        )(intent_out)  # (batch_size, hidden_size)
        intent_out = Dense(
            self.preprocessor.n_intents, activation='sigmoid', name='intent'
        )(intent_out)  # (batch_size, n_intents)

        # Another network for NER.

        tags_out = token_embeddings
        tags_out = model_bodies[self.body](
            num_blocks=self.n_hidden_layers,
            units=self.hidden_size,
            dropout=self.dropout,
            l2=self.l2_regularization,
            return_sequences=True
        )(tags_out)  # (batch_size, max_seq_len, hidden_size)
        tags_out = TimeDistributed(Dense(self.preprocessor.n_tags, activation='sigmoid'))(tags_out)
        tags_out = Lambda(lambda x: x, name='tags')(tags_out)

        self.model = Model(inputs=[in_id, in_mask], outputs=[intent_out, tags_out])
        self._compile_model()

    def _compile_model(self):
        optimizer = tf.keras.optimizers.Adam(self.learning_rate)
        losses = {
            'tags': 'binary_crossentropy',
            'intent': 'binary_crossentropy'
        }
        loss_weights = {'tags': 3.0, 'intent': 1.0}
        metrics = {'intent': 'acc', 'tags': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        self.model.summary(print_fn=logger.debug)

    def train(self, nlu_data: NLUExampleDataset) -> float:
        """Processes the agent's NLU data into training data, and trains the model.
        """
        start = time()

        if self.balance_intent:
            nlu_data = nlu_data.balance()
        self.preprocessor.fit(nlu_data)
        dataset = tf.data.Dataset.from_tensor_slices(self.preprocessor.transform(nlu_data))

        train_data, val_data, hparams, callbacks = AutoSetup.get_training_setup(self.auto, dataset, self.get_params())
        self.set_params(**hparams)

        self._fit_tf_model(train_data, val_data, callbacks)

        self._fitted = True

        if self.save_model_dir is not None:
            # Save the model's state, so it can be deployed and used.
            self.to_dir(self.save_model_dir)

        train_time = time() - start
        logger.info("Total train time: {:.6f} seconds.", train_time)

        return train_time

    def _fit_tf_model(
        self,
        train_data: tf.data.Dataset,
        val_data: tf.data.Dataset = None,
        callbacks: list = None,
        tensorboard: bool = True
    ) -> None:
        """
        Fits the model on `train_data`, using optional `val_data` for validation.
        `train_data` and `val_data` should be passed in unbatched.
        """
        logger.debug("Fitting model using hyperparameters:")
        logger.debug(self.get_params())

        self._build_and_compile_model()

        if callbacks is None:
            callbacks = []

        if val_data:
            val_data = val_data.batch(self.batch_size)

        if tensorboard:
            logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
            callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=logdir))

        n_train = sum(1 for _ in train_data)

        self.model.fit(
            train_data.batch(self.batch_size),
            epochs=self.epochs,
            steps_per_epoch=AutoSetup.get_steps_per_epoch(n_train, self.batch_size),
            validation_data=val_data,
            use_multiprocessing=True,
            callbacks=callbacks
        )

    def evaluate(
        self,
        nlu_data: NLUExampleDataset,
        *,
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        do_error_analysis: bool = False
    ) -> tuple:
        """
        Performs cross validation to evaluate the model's training set performance
        and generalizable performance on `nlu_data`.

        Parameters
        ----------
        nlu_data : NLUExampleDataset
            NLU example data to train and evaluate on.
        test_ratio : float
            If provided, a basic stratified train/test split will be used.
        nfolds : int
            If provided, stratified k-fold cross validation will be conducted with `k==nfolds`.
        repeat : int
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        do_error_analysis : bool
            Possible only when doing k-fold CV with no repeats. Performs on error analysis on
            all the hold-out folds.

        Returns
        -------
        training_performance : dict
            The metrics from evaluating the fitted model on the training set.
        test_performance : dict
            The metrics from evaluating the fitted model on the test set.
        """
        if test_ratio is not None and nfolds is not None:
            raise ValueError("please supply either test_ratio or nfolds, but not both")
        if do_error_analysis and repeat > 0:
            raise ValueError("an error analysis can only be done when there are no repeats")
        if do_error_analysis and nfolds is None:
            raise ValueError("an error analysis can only be done with k-fold CV")

        if test_ratio is not None:
            eval_fn = lambda: self._evaluate_train_test(nlu_data, test_ratio)
        elif nfolds is not None:
            eval_fn = lambda: self._evaluate_kfold_cv(nlu_data, nfolds, do_error_analysis)
        else:
            raise ValueError("please supply either test_ratio or nfolds")

        if repeat > 0:
            results = [eval_fn() for _ in range(repeat)]
            return tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))
        else:
            return eval_fn()

    def error_analysis(self, nlu_data: NLUExampleDataset) -> list:
        """Predicts on `nlu_data`, then determines which misclassifications were made.

        Returns
        -------
        list
            A list of instance error analyses. Each entry contains data about
            what the ground truth was, what the predictions were, and whether the
            model got the predictions correct or not.
        """
        preds = self.predict([instance.text for instance in nlu_data])
        return [
            {
                "prediction": pred,
                "instance": instance,
                "correct": {
                    "intent": pred.intent.value == instance.intent,
                    # @TODO: This tags comparison will need to be more granular
                    # once we care more about tags.
                    "tags": set(
                        tag.tagType for tag in pred.tags
                    ) == set(
                        tag.tagType for tag in instance.tags
                    )
                }
            } for pred, instance in zip(preds.predictions, nlu_data)
        ]

    def _evaluate_train_test(self, nlu_data: NLUExampleDataset, test_ratio: float) -> tuple:
        # Evaluate the model on a basic train/test split.
        train_nlu_data, test_nlu_data = nlu_data.split(test_ratio)
        return self._evaluate(train_nlu_data, test_nlu_data)

    def _evaluate_kfold_cv(self, nlu_data: NLUExampleDataset, nfolds: int, do_error_analysis: bool = False) -> tuple:
        # Evaluate the model using k-fold cross validation.
        results = []
        error_analysis = []
        for train, test in nlu_data.cv(nfolds):
            results.append(self._evaluate(train, test))
            if do_error_analysis:
                error_analysis += self.error_analysis(test)

        # Now average the k performance results.
        train_performance, test_performance = tuple(aggregate_dicts(dicts, "mean") for dicts in zip(*results))
        if do_error_analysis:
            test_performance["error_analysis"] = error_analysis

        return train_performance, test_performance

    def _evaluate(self, train_nlu_data: NLUExampleDataset, test_nlu_data: NLUExampleDataset) -> tuple:
        train_time = self.train(train_nlu_data)

        train_performance = self.score(train_nlu_data)
        train_performance["train_time"] = train_time

        test_performance = self.score(test_nlu_data)

        # Get ECE
        ece_quantiles = self.bayesian_ece_for_obj(
            test_nlu_data,
            "intent",
            quantiles=[10, 50, 90],
            is_sparse=False
        )
        for quantile, value in ece_quantiles.items():
            test_performance[f"intent_test_ece_q{quantile}"] = value

        return train_performance, test_performance

    def score(self, nlu_data: NLUExampleDataset) -> dict:
        """Predict the fitted model on `nlu_data`, returning its performance on it.
        """
        assert self._fitted
        dataset = tf.data.Dataset.from_tensor_slices(self.preprocessor.transform(nlu_data))
        return self.model.evaluate(dataset.batch(self.batch_size_predict), return_dict=True)

    def predict(self, instances: t.List[str]) -> NLUPredictions:
        assert self._fitted

        X = self.preprocessor.transform_utterances(instances)
        raw_intent_preds, raw_tags_preds = self.model.predict(
            {"input_ids": X.input_ids, "input_mask": X.attention_mask}
        )

        intents = self._decode_intents(raw_intent_preds)
        tags_by_instance = self.preprocessor.decode_tags(raw_tags_preds, X, instances)

        predictions = [NLUPrediction(intent=intent, tags=tags) for intent, tags in zip(intents, tags_by_instance)]

        return NLUPredictions(predictions=predictions)

    def _decode_intents(self, raw_intent_prediction: np.ndarray) -> t.List[StrPredWithConf]:
        intent_label_indices = np.argmax(raw_intent_prediction, axis=-1)
        confidences = np.max(raw_intent_prediction, axis=-1)
        intents = self.preprocessor.intents_encoder.inverse_transform(intent_label_indices)
        return [StrPredWithConf(value=intent, confidence=conf.item()) for intent, conf in zip(intents, confidences)]

    def bayesian_ece_for_obj(
        self,
        nlu_data: NLUExampleDataset,
        obj: str,
        *,
        quantiles: t.Sequence = [10, 50, 90],
        bins: int = 15,
        is_sparse: bool = True
    ) -> t.Dict[int, float]:
        """
        Computes the Bayesian Expected Calibration Error (ECE) for `data` (ubatched)
        with respect to a single objective of the model (denoted by `obj`). Returns
        the quantiles denoted by `quantiles` of the approximated posterier bayesian
        distribution over ECE. If the labels in `data` are sparse, `is_sparse` should be
        `True`.
        """
        assert self._fitted
        dataset = tf.data.Dataset.from_tensor_slices(self.preprocessor.transform(nlu_data))
        y_pred = self.model.predict(dataset.batch(self.batch_size_predict), verbose=1)

        # Isolate the labels and predictions for the objective in question.
        y_obj = tf.stack([y[obj] for _, y in dataset])
        if not is_sparse:
            # The ECE equation expects sparse labels.
            y_obj = tf.argmax(y_obj, axis=-1)

        obj_i = self.model.output_names.index(obj)
        y_pred_obj = tf.convert_to_tensor(y_pred[obj_i], tf.float32)

        ece_samples = um.bayesian_expected_calibration_error(
            bins,
            probabilities=y_pred_obj,
            labels_true=tf.cast(y_obj, tf.int32)
        )
        ece_quantiles = tfp.stats.percentile(ece_samples, quantiles)
        return {quantile: float(value) for quantile, value in zip(quantiles, ece_quantiles)}

    @classmethod
    def tune(
        cls,
        nlu_data: NLUExampleDataset,
        *,
        val_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        **tune_args
    ):
        def objective(model: NLUModel) -> dict:
            train_perf, test_perf = model.evaluate(nlu_data, test_ratio=val_ratio, nfolds=nfolds, repeat=repeat)
            results = {}
            for k, v in train_perf.items():
                results[f"train_{k}"] = v
            for k, v in test_perf.items():
                results[f"test_{k}"] = v
            return results

        super().tune(
            objective_name="test_intent_acc",
            objective=objective,
            mode="max",
            **tune_args
        )
