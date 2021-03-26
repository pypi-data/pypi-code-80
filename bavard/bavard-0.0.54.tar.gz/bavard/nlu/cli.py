import json
import os

from bavard_ml_common.types.agent import AgentExport

from bavard.config import logger

from bavard.nlu.model import NLUModel


class NLUModelCLI:
    """Tools useful for local development and ad-hoc architecture search of NLU models.
    """

    @staticmethod
    def evaluate(
        agent_data_file: str,
        *,
        test_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        do_error_analysis: bool = False,
        write_path: str = None,
        **nlu_model_args
    ):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to evaluate on.
        test_ratio : float, optional
            The percentage of the dataset to use as a test set, if evaluating
            via a train/test split.
        nfolds : int, optional
            The number of folds to do, if evaluating via k-fold cross validation.
        repeat : int, optional
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        do_error_analysis : bool, optional
            Possible only when doing k-fold CV with no repeats. Performs on error analysis on
            all the hold-out folds.
        write_path : str, optional
            If supplied, the results will be written out to the `write_path` directory.
        **nlu_model_args : optional
            Any control parameters or hyperparameters to pass to NLUModel
            constructor. If `auto==True`, some of these values may be
            overridden.
        """
        data = AgentExport.parse_file(agent_data_file).config.to_nlu_dataset()
        model = NLUModel(**nlu_model_args)
        train_performance, test_performance = model.evaluate(
            data,
            test_ratio=test_ratio,
            nfolds=nfolds,
            repeat=repeat,
            do_error_analysis=do_error_analysis
        )
        logger.info("train performance: {}", train_performance)
        logger.info("test performance: {}", test_performance)
        if write_path:
            with open(os.path.join(write_path, "train-performance.json"), "w") as f:
                json.dump(train_performance, f)
            with open(os.path.join(write_path, "test-performance.json"), "w") as f:
                json.dump(test_performance, f)

    @staticmethod
    def train(agent_data_file: str, **nlu_model_args):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to train on.
        **nlu_model_args : optional
            Any control parameters or hyperparameters to pass to NLUModel
            constructor. If `auto==True`, some of these values may be
            overridden.
        """
        data = AgentExport.parse_file(agent_data_file).config.to_nlu_dataset()
        model = NLUModel(**nlu_model_args)
        model.train(data)

    @staticmethod
    def predict(
        model_path: str,
        *,
        batch_file: str = None,
        interactive: bool = False
    ):
        """
        Parameters
        ----------
        model_path : str
            Path to the saved model that will be loaded.
        batch_file : str, optional
            Pass this file path to predict on a file of text; one prediction per line.
        interactive : bool, optional
            If supplied, interact with the model, providing inputs for prediction via CLI.
        """
        model = NLUModel.from_dir(model_path)
        if batch_file:
            with open(batch_file) as f:
                utterances = [utterance.replace("\n", "") for utterance in f]
            print(model.predict(utterances))

        if interactive:
            quits = {"q", "quit", "exit"}
            while True:
                utterance = input("\nEnter your utterance ('q' to quit) >>> ")
                if utterance in quits:
                    break
                print(model.predict([utterance]))

    @staticmethod
    def tune(
        agent_data_file: str,
        *,
        val_ratio: float = None,
        nfolds: int = None,
        repeat: int = 0,
        **tune_args
    ):
        """
        Parameters
        ----------
        agent_data_file : str
            Path to the agent data file to evaluate on.
        val_ratio : float, optional
            The percentage of the dataset to use as a test set, if evaluating
            via a train/test split.
        nfolds : int, optional
            The number of folds to do, if evaluating via k-fold cross validation.
        repeat : int, optional
            If > 0, the evaluation will be performed `repeat` times and results will be
            averaged. This is useful when you want to average out the variance caused by
            random weight initialization, etc.
        **tune_args : kwargs, optional
            Any other arguments to pass to the underlying tune method.
        """
        data = AgentExport.parse_file(agent_data_file).config.to_nlu_dataset()
        NLUModel.tune(
            data,
            val_ratio=val_ratio,
            nfolds=nfolds,
            repeat=repeat,
            **tune_args
        )
