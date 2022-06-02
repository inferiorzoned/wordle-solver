import pandas as pd

# letterPosFreqScores: 5 rows (positions), 26 columns (letters)
letterPosFreqScoresCSV = pd.read_csv('../scorer/scoring utils/weighted_freqs_letters_positions.csv')
# letterAppearFreqScores: 26 columns (letters)
letterAppearFreqScoresCSV = pd.read_csv('../scorer/scoring utils/letter_total_weights.csv')
# allWordsScores: 12972 rows (words), 2 columns (scores)
# allWordsScoresCSV = pd.read_csv('../scorer/scoring utils/all_words_scores.csv')
allWordsScoresCSV = pd.read_csv('../scorer/scoring utils/all_words_scores_wordle.csv')

def precalculateScores():
    global allWordsScoresDict
    # convert allWordsScores to a dictionary in one line
    allWordsScoresDict = dict(zip(allWordsScoresCSV['Word'], allWordsScoresCSV['Score']))

def getMostScoredLetter(letters):
    highestScore = 0
    highestLetter = None
    letterAppearFreqScores = letterAppearFreqScoresCSV.values
    for letter in letters:
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        if letterAppearFreqScores[0][letter] > highestScore:
            highestScore = letterAppearFreqScores[0][letter]
            highestLetter = letter
    return chr(highestLetter + ord('a')) if highestLetter is not None else ""

def getMostScoredVowel(letters):
    highestScore = 0
    highestLetter = None
    letterAppearFreqScores = letterAppearFreqScoresCSV.values
    for letter in letters:
        # check if the letter is a vowel
        if letter.lower() in ['a', 'e', 'i', 'o', 'u']:
            # convert the letter to value of 0 - 25
            letter = ord(letter) - ord('a')
            if letterAppearFreqScores[0][letter] > highestScore:
                highestScore = letterAppearFreqScores[0][letter]
                highestLetter = letter
    if highestLetter is not None:
        return chr(highestLetter + ord('a'))
    else:
        return ""

# print(getMostScoredLetter('abcdefghijklmnopqrstuvwxyz'))

def scoreAWord(word):
    # using static dictionary of precalculated scores
    return allWordsScoresDict[word]

    # runtime scoring (if dynamic scoring is needed)
    # but using static dictionary of precalculated scores right now
    # letterPosFreqScores = letterPosFreqScoresCSV.values
    # posFreqScore = 0
    # for idx, letter in enumerate(word):
    #     # convert the letter to lowercase
    #     letter = letter.lower()
    #     # convert the letter to value of 0 - 25
    #     letter = ord(letter) - ord('a')
    #     # increment the score
    #     posFreqScore += letterPosFreqScores[idx][letter]    

    # letterAppearFreqScores = letterAppearFreqScoresCSV.values
    # appearFreqScore = 0
    # for letter in word:
    #     # convert the letter to lowercase
    #     letter = letter.lower()
    #     # convert the letter to value of 0 - 25
    #     letter = ord(letter) - ord('a')
    #     # increment the score
    #     appearFreqScore += letterAppearFreqScores[0][letter]

    # return posFreqScore + appearFreqScore

class WordleScorer:
    def __init__(self, validWords):
        self.validWords = validWords

    def scoreAllWords(self):
        self.wordScores = {}
        for word in self.validWords:
            self.wordScores[word] = scoreAWord(word)
        return self.wordScores

# precalculateScores()
# print(scoreAWord('sales'))






