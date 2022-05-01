import pandas as pd
import os

def scoreAWord(word):
    # letterPosFreqScores: 5 rows (positions), 26 columns (letters)
    # print(os.path.abspath('scoring utils/weighted_freqs_letters_positions.csv'))
    # letterPosFreqScores = pd.read_csv(os.path.abspath('scoring utils/weighted_freqs_letters_positions.csv'))
    letterPosFreqScores = pd.read_csv('scorer/scoring utils/weighted_freqs_letters_positions.csv')
    # letterAppearFreqScores: 26 columns (letters)
    letterAppearFreqScores = pd.read_csv('scorer/scoring utils/letter_total_weights.csv')

    letterPosFreqScores = letterPosFreqScores.values
    posFreqScore = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the score
        posFreqScore += letterPosFreqScores[idx][letter]
    print(posFreqScore)

    letterAppearFreqScores = letterAppearFreqScores.values
    appearFreqScore = 0
    for letter in word:
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the score
        appearFreqScore += letterAppearFreqScores[0][letter]
    print(appearFreqScore)

    return posFreqScore + appearFreqScore

class WordleScorer:
    def __init__(self, validWords):
        self.validWords = validWords

    def scoreAllWords(self):
        self.wordScores = {}
        print(len(self.validWords))
        for word in self.validWords:
            self.wordScores[word] = scoreAWord(word)
        print(self.wordScores)
        return self.wordScores

# scoreAWord('hello')






