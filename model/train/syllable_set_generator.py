from transform import syllable
from utils import utils
import sys
import itertools


def main():
    #dir_ = sys.argv[1]
    dir_ = '/Users/alexander/Diploma/txt_acc_nkrja/'
    files = utils.read_dataset(dir_)
    all_syllables = dict()
    all_syllables['UNC'] = 0
    all_syllables['SEP'] = 1
    all_syllables['END'] = 2
    all_syllables['START'] = 3
    print(len(files))
    for word in itertools.chain.from_iterable(files):
        for syl in syllable.SyllableTrasformer.word_to_syllables(word.replace("'", '').lower()):
            if syl not in all_syllables:
                all_syllables[syl] = len(all_syllables)
        for syl in syllable.SyllableTrasformer.word_to_syllables(word.replace("'", '')):
            if syl not in all_syllables:
                all_syllables[syl] = len(all_syllables)
    with open('Syllables.dict', 'w') as dict_file:
        for x in all_syllables:
            dict_file.write('{}${}\n'.format(x, all_syllables[x]))


if __name__ == "__main__":
    main()