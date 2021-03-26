from abc import ABC, abstractmethod
import typing as t

import kerastuner as kt
import tensorflow as tf
from bavard.config import logger


class TFTunable(ABC):
    """A Tensorflow model class can implement this abstract class to automatically get hyperparameter tuning behavior.
    """

    @staticmethod
    @abstractmethod
    def get_hp_spec(hp: kt.HyperParameters) -> t.Dict[str, kt.engine.hyperparameters.HyperParameter]:
        """
        In order to support hyperparameter tuning, this method should be implemented which
        accepts a kerastuner hyperparameter sampling argument `hp`, and returns a mapping
        of all this model's hyperparameter names to their sampling specification. See
        https://keras-team.github.io/keras-tuner/documentation/hyperparameters/ for more
        info.
        """
        pass

    @classmethod
    def tune(
        cls,
        *,
        objective_name: str,
        objective: t.Callable[["TFTunable"], dict],
        mode: str,
        strategy: str = "bayesian",
        max_trials: int = 100,
        callbacks: t.Optional[t.Sequence[t.Callable]] = None,
        project_name: t.Optional[str] = None,
        use_wandb: bool = False
    ):
        """
        Performs hyperparameter optimization of the model according to `objective`.

        Parameters
        ----------
        objective_name : str
            The name of the quantity to optimize.
        objective : callable
            A function which should accept an instance of this class and return a dictionary.
            The dictionary must contain the `objective_name` key and have the value to optimize
            as that key's value.
        mode : str
            One of `"max"` or `"min"`. Represents the direction of optimization i.e. should we
            maximize or minimize the objective.
        strategy : str, optional
            The optimization strategy to use.
        max_trials : int, optional
            The maximum number of optimization trials to run.
        callbacks : sequence of callables, optional
            Optional callback functions that will be invoked at the end of every tuning trial.
            Each is invoked with the parameters `callback(model: BaseModel, objective(model))`,
            which yields the model from the completed trial, as well as the results dictionary from
            the objective function computed for that model.
        project_name : str, optional
            Optional name for the project. If provided, the KerasTuner trial results will be
            saved under a directory of this name. If not provided, they will be saved under
            a default directory `"untitled_project"`.
        use_wandb : bool, optional
            Whether to log each trial's results to a Weights and Biases project. If `True`,
            `project_name` must also be set.
        """
        assert mode in {"min", "max"}
        if callbacks is None:
            callbacks = []
        if use_wandb and project_name is None:
            raise ValueError("project_name must be specified when use_wandb==True")
        if use_wandb:
            wandb_client = WandbClient(project_name)
            callbacks.append(wandb_client.log_model)

        hypermodel = HyperModel(cls)
        tuner = ModelTuner(
            hypermodel,
            objective_name=objective_name,
            objective=objective,
            mode=mode,
            strategy=strategy,
            max_trials=max_trials,
            project_name=project_name
        )
        tuner.search(callbacks=callbacks)

        logger.info("Tuning Results:")
        tuner.results_summary()

        best_hps, = tuner.get_best_hyperparameters()
        logger.info("Best hyperparameters found:")
        logger.info(best_hps.values)

    def get_params(self) -> dict:
        return {name: getattr(self, name) for name in self.get_hp_spec(kt.HyperParameters())}

    def set_params(self, **params):
        param_names = self.get_params().keys()
        for k, v in params.items():
            if k not in param_names:
                raise ValueError(f"{k} is not a known hyperparameter")
            setattr(self, k, v)


class HyperModel(kt.HyperModel):

    def __init__(self, model_cls: t.Type[TFTunable]) -> None:
        super().__init__()
        self._model_cls = model_cls

    def build(self, hp: kt.HyperParameters) -> TFTunable:
        """
        Builds, compiles, and returns a new `self._ModelClass` instance. Uses
        `kerastuner` Hyperparameter objects as the model hyperparameters,
        so it can be searched via hyperparameter optimization.
        """
        return self._model_cls(**self._model_cls.get_hp_spec(hp))


class ModelTuner(kt.engine.base_tuner.BaseTuner):
    strategy_map = {
        "bayesian": kt.oracles.BayesianOptimization,
        "random": kt.oracles.RandomSearch
    }

    def __init__(
        self,
        hypermodel: HyperModel,
        *,
        objective_name: str,  # the name of the value we're trying to optimize e.g. 'accuracy'
        objective: t.Callable[[TFTunable], dict],  # the function which takes the model and computes the objective
        mode: str = "max",
        strategy: str = "bayesian",
        max_trials: int = 100,
        project_name: t.Optional[str] = None
    ) -> None:
        super().__init__(
            oracle=self.strategy_map[strategy](
                objective=kt.Objective(objective_name, mode), max_trials=max_trials
            ),
            hypermodel=hypermodel,
            project_name=project_name
        )
        self._objective_name = objective_name
        self._objective = objective

    def run_trial(self, trial, callbacks: t.List[t.Callable]) -> None:
        model: TFTunable = self.hypermodel.build(trial.hyperparameters)
        results = self._objective(model)
        for callback in callbacks:
            callback(model, results)
        tf.keras.backend.clear_session()
        del model
        self.oracle.update_trial(trial.trial_id, {self._objective_name: results[self._objective_name]})


class WandbClient:
    """Client for logging kerastuner results to a Weights and Biases project.
    """

    def __init__(self, project: str):
        import wandb
        self._project = project
        self._wandb = wandb

    def log_model(self, model: TFTunable, trial_results: dict, **other_config_values):
        with self._wandb.init(project=self._project, reinit=True) as run:
            # Log the hyperparameter values
            run.config.update(model.get_params())
            # Log the model's performance and other config
            run.config.update(other_config_values)
            run.summary.update(trial_results)
