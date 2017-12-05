from transform import encoding
from keras import losses
from keras.utils import to_categorical
import tensorflow as tf

def train_on_batch(model, syll_dictionary, batch, optimizer, max_len):
    encoded_batch = to_categorical(encoding.encode_batch(batch[0], syll_dictionary), len(syll_dictionary))
    answer = model.predict(encoded_batch)

    loss = losses.categorical_crossentropy(to_categorical(batch[1], max_len), answer)
    train_step = tf.train.AdamOptimizer().minimize(loss, var_list=[model.weights])
    return train_step

def get_score(model, syll_dictionary, batch):
    encoded_batch = to_categorical(encoding.encode_batch(batch[0], syll_dictionary), len(syll_dictionary))
    answer = model.predict(encoded_batch)
    return tf.metrics.accuracy(batch[1], tf.argmax(answer, 1))

