import pandas as pd

def scoreAWord(word):
    """
    Scores a word according to the scoring values of the letters
    : param word: the word to be scored
    """
    # letterPosFreqScores: 5 rows (positions), 26 columns (letters)
    letterPosFreqScores = pd.read_csv('../scorer/scoring utils/weighted_freqs_letters_positions.csv')
    # letterAppearFreqScores: 26 columns (letters)
    letterAppearFreqScores = pd.read_csv('../scorer/scoring utils/letter_total_weights.csv')

    letterPosFreqScores = letterPosFreqScores.values
    posFreqScore = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the score
        posFreqScore += letterPosFreqScores[idx][letter]    

    letterAppearFreqScores = letterAppearFreqScores.values
    appearFreqScore = 0
    for letter in word:
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the score
        appearFreqScore += letterAppearFreqScores[0][letter]

    return posFreqScore + appearFreqScore

class WordleScorer:
    def __init__(self, validWords):
        self.validWords = validWords

    def scoreAllWords(self):
        """
        Scores all the words in the wordlist
        """
        self.wordScores = {}
        for word in self.validWords:
            self.wordScores[word] = scoreAWord(word)
        return self.wordScores

# scoreAWord('hello')






