import numpy as np

from utils import utils

def prepare_batch(dataset, batch_size):
    indeces = np.random.randint(0, len(dataset), batch_size)
    return [dataset[i] for i in indeces]


