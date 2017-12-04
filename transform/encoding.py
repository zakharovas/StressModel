import numpy as np
from transform import syllable


def encode_phrase(phrase, syl_dict, sep=' '):
    words = phrase.split(sep)
    encoded = [syl_dict.get_begin()]

    for word in words:
        syllables = syllable.SyllableTrasformer.word_to_syllables(word)
        for syl in syllables:
            if syl in syl_dict:
                encoded.append(syl_dict[syl])
            else:
                encoded.append(syl_dict.get_unc())
        encoded.append(syl_dict.get_sep())
    encoded = encoded[:-1] + [syl_dict.get_end()]
    return encoded


def encode_batch(batch):
    return np.array([encode_phrase(phrase) for phrase in batch])
