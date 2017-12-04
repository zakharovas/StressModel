import re

class SyllableTrasformer:
    VOWELS = 'аеиоуэюяыё'
    SEPARATOR = '\t'

    # https://ru.wikipedia.org/wiki/Слог#Слогоделение_в_русском_языке
    @staticmethod
    def word_to_syllables(word):
        number_of_syllables = len(re.findall('[' + SyllableTrasformer.VOWELS + ']',
                                         word, re.IGNORECASE))

    
