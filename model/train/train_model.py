from keras import losses
import tensorflow as tf
from sklearn.metrics import accuracy_score
import numpy as np


def create_training(model, optimizer, max_len, session):
    input_seq = tf.placeholder('int32', [None, None])
    predictions = model.predict(input_seq)
    answers = tf.placeholder('int32', [None])
    loss = tf.reduce_sum(tf.reduce_sum(losses.categorical_crossentropy(tf.one_hot(answers, max_len), predictions)))
    train_step = optimizer.minimize(loss, var_list=[model.weights])

    def train_on_batch(batch):
        return session.run([loss, train_step], {input_seq: batch[0], answers: batch[1]})
    return train_on_batch


def creacte_predictor(model, session):
    input_seq = tf.placeholder('int32', [None, None])
    answer = model.predict(input_seq)

    def predict_stress(data):
        return session.run(answer, {input_seq : data})
    return predict_stress


def get_score(data, predictor):
    predictions = predictor(data[0])
    return accuracy_score(np.argmax(data[1], 1), np.argmax(predictions, 1))

