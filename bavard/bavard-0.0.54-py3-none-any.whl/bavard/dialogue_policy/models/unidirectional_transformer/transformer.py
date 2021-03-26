import tensorflow as tf

from bavard.dialogue_policy.models.unidirectional_transformer.encoder import Encoder


class Transformer(tf.keras.Model):
    def __init__(self, num_layers, d_model, num_heads, dff, input_vocab_size,
                 target_vocab_size, pe_input, rate=0.1):
        super(Transformer, self).__init__()

        self.encoder = Encoder(num_layers, d_model, num_heads, dff,
                               input_vocab_size, pe_input, rate)

        self.final_layer = tf.keras.layers.Dense(target_vocab_size)

    def call(self, inp, tar, training, enc_padding_mask, look_ahead_mask):
        # # @TODO
        # enc_output = self.encoder(inp, training, enc_padding_mask)  # (batch_size, inp_seq_len, d_model)
        #
        # final_output = self.final_layer(dec_output)  # (batch_size, tar_seq_len, target_vocab_size)
        #
        # return final_output, attention_weights
        pass
