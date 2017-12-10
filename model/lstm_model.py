import keras.layers as L
import tensorflow as tf

from model import attention_layer


class BidirectionalLSTMModel:

    def __init__(self, name, syllables, emb_size, hid_size, out_size):
        self.name = name
        self.syllables = syllables
        with tf.variable_scope(name):
            self.emb_inp = L.Embedding(len(syllables) + 2, emb_size)
            self.enc_forward = tf.nn.rnn_cell.LSTMCell(hid_size/2)
            self.enc_back = tf.nn.rnn_cell.LSTMCell(hid_size/2)
            self.out_layer = L.Dense(out_size, activation='softmax')
            self.transform = L.Dense(hid_size)
            self.attn = attention_layer.AttentionLayer(name, hid_size, hid_size, hid_size)
            # weight initialization
            batch = tf.placeholder('int32', [None, None])
            mask = tf.placeholder('int32', [None, None])
            states, out_state = self._encode(batch)
            out_state = self.transform(out_state)
            h1 = self._predict(states, out_state, mask)
        self.weights = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=name)

    def _encode(self, batch):
        lengths = self._get_lengths(batch, self.syllables.get_end_char())
        embedinng = self.emb_inp(batch)
        (forw_out, back_out), (forw_state, back_state) = tf.nn.bidirectional_dynamic_rnn(
            self.enc_forward, self.enc_back, embedinng,
            sequence_length=lengths,
            dtype=embedinng.dtype)
        out_h = tf.concat((forw_state.h, back_state.h), 1)
        concat_output = tf.concat((forw_out, back_out), 2)
        return concat_output, out_h

    def _predict(self, states, start_state, mask):
        attn, probs = self.attn(states, start_state, mask)
        return self.out_layer(attn), probs

    def predict_with_attention(self, batch):
        mask = self._get_mask(batch, self.syllables.get_end_char())
        states, out_state = self._encode(batch)
        return self._predict(states, out_state, mask)

    def predict_without_attention(self, batch):
        return self.predict_with_attention(batch)[0]

    def predict(self, batch):
        return self.predict_without_attention(batch)

    @staticmethod
    def _get_lengths(batch, end_char):
        is_end = tf.cast(tf.equal(batch, end_char), tf.int32)
        sentence_mask = tf.cumsum(is_end, axis=1, exclusive=True)
        lengths = tf.reduce_sum(tf.cast(tf.equal(sentence_mask, 0), tf.int32), axis=1)
        return lengths

    @staticmethod
    def _get_mask(batch, end_char):
        lengths = BidirectionalLSTMModel._get_lengths(batch, end_char)
        return tf.sequence_mask(lengths, maxlen=tf.shape(batch)[1], dtype=tf.float32)
