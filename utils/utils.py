import os
import re
from transform import syllable

def prepare_file(file):
    separators = r'[!\.\?,‘’“”„…–—"\(\):;\[\]\\{}«»\-]+'
    non_cyrillic = r'[\&\*0-9<>=@A-Za-z^`_|¬ії№#$%]+'
    file = ' '.join(file.split())
    separators_expression = re.compile(separators)
    non_cyrillic_expression = re.compile(non_cyrillic)
    sentences = separators_expression.split(non_cyrillic_expression.sub('', file))
    sentences = filter(lambda x: len(x) > 0, sentences)
    return [sentence.replace('--', '').split() for sentence in sentences]

def read_dataset(root):
    dirs = os.walk(root)
    files = []
    for dir in dirs:
        for file in dir[2]:
            if (file[-4:] == '.txt'):
                with open(os.path.join(dir[0], file), 'r') as input_file:
                    file_as_str = input_file.read()
                    files += prepare_file(file_as_str)
    return files


def read_file(filename):
    with open('r', filename) as input_file:
        input_file.read()


def find_stress(word):
    position = word.find("'")
    if position == -1 or len(word) < 2:
        return -1
    word = word.replace("'", '')
    syllables = syllable.SyllableTrasformer.word_to_syllables(word)
    cur_length = 0
    for i, syl in enumerate(syllables):
        cur_length += len(syl)
        if cur_length + 1 >= position:
            return i
