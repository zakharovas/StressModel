from transform import syllable
from utils import utils
import sys
import itertools


def main():
    files = utils.read_dataset(sys.argv[1])
    all_syllables = dict()
    all_syllables['UNC'] = 0
    all_syllables['SEP'] = 1
    all_syllables['END'] = 2
    all_syllables['START'] = 3
    for word in itertools.chain.from_iterable(files):
        for syl in syllable.SyllableTrasformer.word_to_syllables(word.replace("'", '').lower()):
            all_syllables[syl] = len(all_syllables)
    with open('Syllables.dict', 'w') as dict_file:
        for x in all_syllables:
            dict_file.write('{}${}\n'.format(x, all_syllables[x]))


if __name__ == "__main__":
    main()