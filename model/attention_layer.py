import tensorflow as tf


class AttentionLayer:
    def __init__(self, name, enc_size, dec_size, hid_size, activ=tf.tanh):
        self.name = name
        self.enc_size = enc_size
        self.dec_size = dec_size
        self.hid_size = hid_size
        self.activ = activ
        with tf.variable_scope(name):
            self.dec = tf.get_variable('att_dec', shape=[dec_size, hid_size])
            self.enc = tf.get_variable('att_enc', shape=[enc_size, hid_size])
            self.vec = tf.get_variable('att_vec', shape=[hid_size, 1])[:, 0]

    def __call__(self, enc, dec, inp_mask):
        with tf.variable_scope(self.name):
            enc_prod = tf.einsum('aij,jk->aik', enc, self.enc)
            dec_prod = tf.matmul(dec, self.dec)
            scores = tf.einsum('aij,j->ai',
                               self.activ(tf.einsum('aij,aj->aij', enc_prod, dec_prod)), self.vec)
            scores = tf.exp(scores)
            scores = scores * tf.to_float(inp_mask)
            probs = tf.einsum('ai,a->ai', scores, 1 / tf.reduce_sum(scores, 1)) + 1e-150
            attn = tf.einsum('aij,ai->aj', enc, probs)

            return attn, probs
