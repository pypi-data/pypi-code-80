import json
from glob import glob
from pprint import pprint
import typing as t

from bavard_ml_common.types.agent import AgentExport
from bavard_ml_common.types.conversations.actions import UserAction, AgentAction
from bavard_ml_common.types.conversations.conversation import ConversationDataset, Conversation
from bavard_ml_common.types.conversations.dialogue_turns import UserDialogueTurn, AgentDialogueTurn

from bavard.common.model_base import WandbClient
from bavard.dialogue_policy.models import Classifier
from bavard.dialogue_policy.models.base import BaseDPModel


class DialoguePolicyModelCLI:
    """
    Tools useful for local development and ad-hoc architecture search of
    dialogue policy models.
    """

    @staticmethod
    def train(agent_data_file: str, save_path: str = None, **modelparams) -> None:
        """Train a model on an agent's training conversations, then optionally save it.

        Parameters
        ----------
        agent_data_file : str
            The path to an agent's JSON data.
        save_path : str, optional
            If provided, the fitted model will be serialized to this path, by default None
        **modelparams : dict
            Any additional control or hyper parameters to pass to the model.
        """
        agent_config = AgentExport.parse_file(agent_data_file).config
        agent_config.clean()
        model = Classifier(**modelparams)
        model.fit(agent_config.to_conversation_dataset())
        if save_path:
            model.to_dir(save_path)

    @staticmethod
    def predict(save_path: str, conversations_path: str = None, interactive: bool = False) -> None:
        """Loads a trained model and predicts next actions on conversations.

        Parameters
        ----------
        save_path : str
            The path to load a serialized model from.
        conversations_path : str, optional
            The path to a JSON file of conversations to predict on.
        interactive : bool, optional
            If True, user will be able to interact directly with the trained model
            at `save_path` by entering user intents in a conversation and seeing
            what the action the dialogue agent would take, given their response.
        """
        model = Classifier.from_dir(save_path)

        if conversations_path:
            with open(conversations_path) as f:
                convs = [Conversation.parse_obj(conv) for conv in json.load(f)]
            print(model.predict(convs))

        if interactive:
            conversation = DialoguePolicyModelCLI._predict_and_add_to_conv(model)
            quits = {"q", "quit", "exit"}
            restarts = {"r", "restart"}
            while True:
                intent = input(
                    f"(turn {len(conversation):2d}) Enter a user "
                    "intent (press 'q' to quit, 'r' to restart conversation) >>> "
                )
                if intent in quits:
                    break
                if intent in restarts:
                    conversation = DialoguePolicyModelCLI._predict_and_add_to_conv(model)
                    continue
                conversation.turns.append(
                    UserDialogueTurn(userAction=UserAction(type="UTTERANCE_ACTION", intent=intent))
                )
                conversation = DialoguePolicyModelCLI._predict_and_add_to_conv(model, conversation)

    @staticmethod
    def _predict_and_add_to_conv(model: BaseDPModel, conv: t.Optional[Conversation] = None) -> Conversation:
        if conv is None:
            conv = Conversation(turns=[])
        pred = model.predict([conv])[0][0]
        print(f"(turn {len(conv):2d}) predicted:", pred)
        conv.turns.append(AgentDialogueTurn(agentAction=AgentAction(type="UTTERANCE_ACTION", name=pred.value)))
        return conv

    @staticmethod
    def evaluate(
        agent_data_file: str,
        *,
        test_ratio: float = None,
        nfolds: int = None,
        wandb_project: str = None,
        **modelparams
    ) -> None:
        """Evaluates a model on an agent's training conversations.

        Parameters
        ----------
        agent_data_file : str
            The path to an agent's JSON data.
        test_ratio : float, optional
            The ratio of the agent's training conversations to use as the test set.
        nfolds : int, optional
            The number of folds to use in a k-fold cross validation scenario.
        wandb_project : str, optional
            If provided, the model's training info and metrics will be logged to this
            Weights & Biases project name.
        **modelparams : dict
            Any additional control or hyper parameters to pass to the model.
        """
        data = AgentExport.parse_file(agent_data_file).config.to_conversation_dataset()

        if wandb_project:
            # Log all results to the Weights and Biases project
            wb = WandbClient(wandb_project)
            model = Classifier(**modelparams)
            scores = model.evaluate(data, test_ratio=test_ratio, nfolds=nfolds)
            wb.log_model(model, scores, test_ratio=test_ratio, nfolds=nfolds)
        else:
            # Just evaluate the model and print the results.
            model = Classifier(**modelparams)
            scores = model.evaluate(data, test_ratio=test_ratio, nfolds=nfolds)
            pprint(scores)

    @staticmethod
    def tune(
        agent_data_file: str,
        *,
        val_ratio: float = None,
        nfolds: int = None,
        **tune_args
    ) -> None:
        data = AgentExport.parse_file(agent_data_file).config.to_conversation_dataset()
        Classifier.tune(data, val_ratio=val_ratio, nfolds=nfolds, **tune_args)

    @staticmethod
    def score(save_path: str, conversations_path: str = None):
        """Scores trained model saved at `save_path` on the conversations saved at `conversations_path`.
        """
        model = Classifier.from_dir(save_path)
        with open(conversations_path) as f:
            raw_convs = json.load(f)
        data = ConversationDataset([Conversation.parse_obj(raw_conv) for raw_conv in raw_convs])
        print(model.score(data))

    @staticmethod
    def aggregate(project_dir: str, topn: int = 5) -> None:
        """
        Aggregate the results of a hyperparameter tuning session, to see which
        hyperparameter configurations resulted in the best scores.

        Parameters
        ----------
        project_dir : str
            The path to the directory containing all the hyperparameter
            optimization trial results.
        topn : int
            The number of top experiments to show.
        """
        files = glob(f"{project_dir}/*/trial.json")
        results = []
        for fname in files:
            with open(fname) as f:
                data = json.load(f)
            if data["status"] == "COMPLETED":
                results.append({
                    "score": data["score"],
                    "hyperparameters": data["hyperparameters"]["values"]
                })

        results.sort(reverse=True, key=lambda r: r["score"])
        for result in results[:topn]:
            pprint(result)
