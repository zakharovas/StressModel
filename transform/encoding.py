import numpy as np

from transform import syllable
from utils import utils


def encode_phrase(phrase, syl_dict, sep=' '):
    print(phrase)
    words = phrase.split(sep)
    encoded = [syl_dict.get_begin_char()]

    for word in words:
        syllables = syllable.SyllableTrasformer.word_to_syllables(word)
        for syl in syllables:
            if syl in syl_dict:
                encoded.append(syl_dict[syl])
            else:
                encoded.append(syl_dict.get_unc_char())
        encoded.append(syl_dict.get_sep_char())
    encoded = encoded[:-1] + [syl_dict.get_end_char()]
    return encoded


def encode_batch(batch, syl_dict):
    return np.array([encode_phrase(phrase, syl_dict) for phrase in batch])


def dataset_to_xy(dataset, suffix_len, syl_dict):
    data = []
    answer = []
    for sentence in dataset:
        for i, word in enumerate(sentence):
            if utils.find_stress(word) >= 0:
                phrase = ''
                prev_length = 1
                position = utils.find_stress(word)
                if i > 0:
                    previous = sentence[i - 1].replace("'", '')[-suffix_len:]
                    prev_length = len(
                        encode_phrase(previous, syl_dict))
                    phrase = previous + ' ' + word.replace("'", '')
                else:
                    phrase = word.replace("'", '')
                if i < len(sentence) - 1:
                    next = sentence[i + 1].replace("'", '')[-suffix_len:]
                    phrase += ' ' + next
                x = encode_phrase(phrase, syl_dict)
                y = position + prev_length
                data.append(x)
                answer.append(y)
            else:
                continue
    return data, answer