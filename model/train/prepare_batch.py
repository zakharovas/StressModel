import numpy as np


def prepare_batch(xs, ys, end_char,  batch_size):
    indeces = np.random.randint(0, len(xs), batch_size)
    batch_x = [xs[i] for i in indeces]
    return conv_to_matrix(batch_x, end_char), [ys[i] for i in indeces]

def conv_to_matrix(xs, end_char):
    max_len = max(map(len, xs))
    matrix = np.zeros((len(xs), max_len)) + end_char
    for i, line in enumerate(xs):
        matrix[i, :len(line)] = line
    return matrix
