import pandas as pd


def scoreAWord(word):
    # letterPosFreqScores: 5 rows (positions), 26 columns (letters)
    letterPosFreqScores = pd.read_csv('weighted_freqs_letters_positions.csv')
    # letterFreqScores: 26 columns (letters)
    letterTotalScores = pd.read_csv('letter_total_weights.csv')

    letterPosFreqScores = letterPosFreqScores.values
    freqScore = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 to 25
        letter = ord(letter) - ord('a')
        # increment the score
        print(idx, letter)
        freqScore += letterPosFreqScores[idx][letter]
    print(freqScore)

    letterTotalScores = letterTotalScores.values
    totalScore = 0
    for letter in word:
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 26
        letter = ord(letter) - ord('a')
        # increment the score
        totalScore += letterTotalScores[0][letter]
    print(totalScore)

class WordleScorer:
    def __init__(self, validWords):
        self.validWords = validWords

scoreAWord('a')




