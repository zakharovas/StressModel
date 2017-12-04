import re


class SyllableTrasformer:
    VOWELS = 'аеиоуэюяыё'
    CONSONANTS = 'йцкнгшщзхфвпрлджчсмтб'
    SEPARATOR = '\t'

    # https://ru.wikipedia.org/wiki/Слог#Слогоделение_в_русском_языке
    @staticmethod
    def word_to_syllables(word):
        number_of_syllables = len(
            re.findall('[' + SyllableTrasformer.VOWELS + ']', word, re.IGNORECASE))
        lower_word = word.lower()
        current_syllable = 1
        current_position = 0
        syllables = []
        last_syllable = ""
        # print(number_of_syllables)
        while current_position < len(word):
            # print("pos {}".format(current_position))
            # print("syl {}".format(current_syllable))
            # print("let {}".format(lower_word[current_position]))
            # print(syllables)
            # print(last_syllable)
            if current_syllable >= number_of_syllables:
                syllables.append(word[current_position:])
                break
            if lower_word[current_position] in SyllableTrasformer.VOWELS:
                last_syllable += word[current_position]
                current_position += 1
                syllable_added = False
                if lower_word[current_position] in SyllableTrasformer.CONSONANTS:
                    if lower_word[current_position] in 'лмнр':
                        position = current_position + 1
                        if lower_word[position] in 'ьъ':
                            position += 1
                        if lower_word[position] in SyllableTrasformer.CONSONANTS and lower_word[position] not in 'лмнр':
                            last_syllable += word[current_position: position]
                            current_position = position
                            syllables.append(last_syllable)
                            last_syllable = ''
                            syllable_added = True
                            current_syllable += 1
                    if lower_word[current_position] == 'й' and lower_word[current_position + 1] in SyllableTrasformer.CONSONANTS:
                        last_syllable += word[current_position]
                        syllables.append(last_syllable)
                        last_syllable = ''
                        current_syllable += 1
                        current_position += 1
                        syllable_added = True
                if not syllable_added:
                    syllables.append(last_syllable)
                    last_syllable = ''
                    current_syllable += 1
            else:
                last_syllable += word[current_position]
                current_position += 1
        return syllables
