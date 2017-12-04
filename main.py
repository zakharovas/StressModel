from transform import syllable

def main():
    a = input()
    print(syllable.SyllableTrasformer.word_to_syllables(a))


if __name__ == "__main__":
    main()