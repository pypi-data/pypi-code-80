import typing as t

import numpy as np
import tensorflow as tf

from bavard.config import logger
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.utils import shuffle as do_shuffle
from bavard_ml_common.types.conversations.conversation import ConversationDataset, Conversation

from bavard.dialogue_policy.data.encode.conversation import ConversationEncoder
from bavard.dialogue_policy.data.utils import EncodingContext, LabelBinarizer, TextEncoder
from bavard.dialogue_policy.data.utils import concat_ndarray_dicts


class PreprocessedTrainingData:
    """
    Class for encoding the conversations of an agent's JSON data into ndarrays
    and tensorflow datasets.
    """

    def __init__(self, convs: ConversationDataset, *, shuffle: bool = True, seed: int = 0):
        """
        Parameters
        ----------
        convs : ConversationDataset
            The training conversations to fit the preprocessor to.
        shuffle : bool, optional
            Whether to shuffle the conversations
        seed : int, optional
            The random seed to use for all stochastic operations in this method.
        """
        self.intents = list(convs.unique_intents())
        self.tag_types = list(convs.unique_tag_types())
        self.slots = list(convs.unique_slots())
        self.actions = list(convs.unique_labels())

        # Field encoders
        self.enc_context = EncodingContext(intent=LabelBinarizer(), action=LabelBinarizer(),
                                           tags=MultiLabelBinarizer(), slots=MultiLabelBinarizer(),
                                           action_index=LabelEncoder(), utterance=TextEncoder())

        self.enc_context.fit(intent=self.intents, action=self.actions, tags=[self.tag_types],
                             slots=[self.slots], action_index=self.actions)

        self.conversations = convs.balance(seed)

        if shuffle:
            self.conversations: t.List[Conversation] = do_shuffle(self.conversations, random_state=seed)

        encoded_convs, self.max_len = self._encode_conversations(self.conversations, training=True)
        self.encoded_convs = self._aggregate_encoded_convs(encoded_convs, training=True)
        self.input_dim = self.encoded_convs['feature_vec'].shape[-1]
        self.num_actions = len(self.actions)
        self.num_intents = len(self.intents)
        self.num_slots = len(self.slots)
        self.num_tag_types = len(self.tag_types)
        self.num_convs = len(self.conversations)

        logger.info('Num actions: {}', self.num_actions)
        logger.info('Num intents: {}', self.num_intents)
        logger.info('Num tags: {}', self.num_tag_types)
        logger.info('Num slots: {}', self.num_slots)
        logger.info('Num encoded conversations: {}', self.num_convs)

    def encode_conversations(self, conversations: t.List[Conversation]) -> t.Dict[str, np.ndarray]:
        """Encode conversations data into a dictionary of numpy arrays ready to pass into a neural net.
        Use this method for inference-time conversation encoding (no training labels).

        Parameters
        ----------
        conversations : t.List[Conversation]
            A list of Conversations.

        Returns
        -------
        t.Dict[str, np.ndarray]
            The dictionary of numpy arrays.
        """
        encoded_convs, _ = self._encode_conversations(conversations, training=False)
        return self._aggregate_encoded_convs(encoded_convs, training=False)

    def _encode_conversations(
        self, conversations: t.List[Conversation], training: bool
    ) -> t.Tuple[t.List[t.Dict[str, np.ndarray]], int]:
        """
        Parameters
        ----------
        conversations : list of Conversation
            The conversations to encode.
        training : bool, optional
            If `True`, the returned data will have a key representing
            the next agent action to take after each turn vector.
        """
        encoded_convs = []
        for conv in conversations:
            encoded_conv = ConversationEncoder.encode(conv, self.enc_context)
            if not training and "action" in encoded_conv:
                # We don't want training-specific labels outside a training context.
                del encoded_conv["action"]
            encoded_convs.append(encoded_conv)

        max_conv_len = max([c['feature_vec'].shape[0] for c in encoded_convs])
        return encoded_convs, max_conv_len

    def _aggregate_encoded_convs(
        self, encoded_convs: t.List[t.Dict[str, np.ndarray]], training: bool
    ) -> t.Dict[str, np.ndarray]:
        """
        Parameters
        ----------
        encoded_convs : list of Conversation
            The encoded conversations to aggregate into a single key:ndarray dataset.
        training : bool, optional
            Should be true if `encoded_convs` were encoded in a training context.
        """
        for conv in encoded_convs:
            conv_len = conv['feature_vec'].shape[0]
            for k, v in conv.items():
                if self.max_len - v.shape[0] < 0:
                    # This sequence is too long, so we need to truncate instead of pad.
                    # Remove elements from the beginning of the sequence.
                    v_final = v[-self.max_len:]
                else:
                    # Pad the conversation feature v with zeros so that all features are the same length.
                    pad_width = [(0, 0)] * v.ndim
                    pad_width[0] = (self.max_len - v.shape[0], 0)  # pre padding along the conv turn dimension
                    v_final = np.pad(v, pad_width=pad_width, constant_values=0)
                conv[k] = v_final

            # Compute a mask for conversation v so that padding is not factored into the loss function.
            mask = np.zeros((self.max_len, 1))
            mask[-conv_len:] = 1
            conv['conversation_mask'] = mask

        for conv in encoded_convs:
            for k, v in conv.items():
                assert v.shape[0] == self.max_len

        result = concat_ndarray_dicts(encoded_convs, new_axis=True)
        if "action" in result:
            # Just have the final agent action of each conversation as
            # the label.
            result["action"] = result["action"][:, -1]
        return result

    def to_classifier_dataset(self) -> tf.data.Dataset:
        """
        Makes a dataset with the next agent action indices as Y and all
        other features as X.
        """
        y_name = "action"
        X = {k: v for k, v in self.encoded_convs.items() if k != y_name}
        y = self.encoded_convs[y_name]
        return tf.data.Dataset.from_tensor_slices((X, y))
