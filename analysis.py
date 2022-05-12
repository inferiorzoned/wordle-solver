# take all words from allFiveLetterWords.txt and create a frequency table of all possitional letters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

wordLength = 5
numberOfLetters = 26


def createFrequencyTable(allWords: list) -> np.array:
    """
    Create a frequency table of all possitional letters
    """
    # create a numpy frequency array of size 5 * 26
    freq = np.zeros((wordLength, numberOfLetters))
    for word in allWordsSorted:
        idx = 0
        for letter in word:
            # convert the letter to lowercase
            letter = letter.lower()
            # convert the letter to value of 0 - 25
            letter = ord(letter) - ord('a')
            # increment the frequency of the letter
            freq[idx][letter] += 1
            # increment the position
            idx += 1
    return freq



def getLetterSummedWeights(freq: np.array) -> dict:
    """
    Return the summed weights of each letter
    """
    summed_weights = {}
    for j in range(numberOfLetters):
        summed_weights[chr(ord('A') + j)] = 0
        for i in range(wordLength):
            summed_weights[chr(ord('A') + j)] += (freq[i][j] / wordLength)
    return summed_weights

def saveLetterFreqWeightsCSV(freq: np.array, filename: str) -> None:
    """
    Save the frequency weights to a file
    (as 26 letters => weighted frequency in 5 positions)
    """
    with open(filename, "w") as f:
        headerList = [chr(i + ord('A')) for i in range(numberOfLetters)]
        df = pd.DataFrame(freq, columns=headerList)
        df.to_csv(f, index=False)

def saveLetterTotalWeightsCSV(letterWeight: dict, filename: str) -> None:
    """
    Save the summed weights of each letter to a CSV file
    (as 26 letters => total weights of 5 positions)
    """
    with open(filename, "w") as f:
        headerList = [chr(i + ord('A')) for i in range(numberOfLetters)]
        # convert letterWeight to a numpy array
        letterWeightArray = np.array([letterWeight[chr(ord('A') + i)] for i in range(numberOfLetters)]).reshape(1, -1)
        df = pd.DataFrame(letterWeightArray, columns=headerList)
        df.to_csv(f, index=False)

def createBarplots(freq: np.array) -> None:
    """
    Create barplots of Percentage of Appearance of letters in word positions
    """
    for n in range(wordLength):
        x_axis = [chr(i + ord('A')) for i in range(numberOfLetters)]
        plt.bar(x_axis, freq[n])
        plt.xlabel("Letters")
        plt.ylabel("Percentage of Appearance")
        plt.title(f"{n+1} Positional Letters")
        plt.show()


def calculateScore(word: str) -> float:
    """
    Calculate the score of a word
    """
    letterPosFreqScores = pd.read_csv('weighted_freqs_letters_positions.csv')
    # letterAppearFreqScores: 26 columns (letters)
    letterAppearFreqScores = pd.read_csv('letter_total_weights.csv')

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

    relativePosFreqScore = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # letterPosFreqScores[idx][letter] divided by sum(letterPosFreqScores[:, letter])
        relativePosFreqScore += (letterPosFreqScores[idx][letter] / letterPosFreqScores[:, letter].sum()) * 100
        # print(chr(letter + ord('a')), letterPosFreqScores[idx][letter], letterPosFreqScores[:, letter].sum(), relativePosFreqScore)

    # print(word, relativePosFreqScore)
    return posFreqScore + appearFreqScore + relativePosFreqScore / 2

print(calculateScore("candy"))

def saveWordScores(word_scores: dict, filename: str) -> None:
    # save all word scores to a file
    with open(filename, "w") as f:
        for word, score in word_scores.items():
            f.write(f"{word} - {score}\n")

def loadWordScoresFromFile(filename: str) -> dict:
    """
    Load the word scores from a file
    """
    word_scores = {}
    with open(filename, "r") as f:
        for line in f:
            word, score = line.split(" - ")
            word_scores[word] = float(score)
    return word_scores


def saveWordScoresCSV(word_scores: dict, filename: str) -> None:
    # save all word scores to a csv file
    with open(filename, "w") as f:
        headerList = ["Word", "Score"]
        # convert word_scores to a 2d numpy array (word, score)
        word_scores_array = np.array([[word, score] for word, score in word_scores.items()])
        df = pd.DataFrame(word_scores_array, columns=headerList)
        df.to_csv(f, index=False)

allWordsSorted = open("allFiveLetterWords.txt").read().splitlines()
freq = createFrequencyTable(allWordsSorted)
"""
# count frequeuncy table to weighted frequency table 
# (probablity of appearance at a particular position in a word)
"""
freq_weights = (freq / freq.sum(axis=1, keepdims=True)) * 100
# saveLetterFreqWeightsCSV(freq_weights, "weighted_freqs_letters_positions.csv")

"""
# calculate the summed weights of each letter 
# (probability of appearance in a word)
"""
letterWeights =  getLetterSummedWeights(freq_weights)
# saveLetterTotalWeightsCSV(letterWeights, "letter_total_weights.csv")
lettersWeightsSorted = {k:v for k, v in sorted(letterWeights.items(), key=lambda item: item[1], reverse=True)}
# print(lettersWeightsSorted)
"""
# create a dict of words from allWordsSorted with scores as values
"""
# word_scores = dict(map(lambda w: (w, calculateScore(w)), allWordsSorted))
# word_scores = {k: v for k, v in sorted(word_scores.items(), key=lambda item: item[1], reverse=True)}
word_scores = loadWordScoresFromFile("allWordsScores.txt")
# saveWordScores(word_scores, "allWordsScores.txt")
# saveWordScoresCSV(word_scores, "allWordsScores.csv")


"""
Starting first two words analysis
"""

def getPossibleFirstWords(word_scores: dict) -> list:
    """
    Return a list of all possible first words
    """
    possibleFirstWords = []
    for word, score in word_scores.items():
        # making sure no duplicate letter in the word, and score is significant
        if len(set(word)) == wordLength and score > 110.0:
            possibleFirstWords.append(word)
    return possibleFirstWords

def findSecondWord(first_word: str, scored_words: tuple) -> tuple:
    """
    Return the (word, score) with the highest score containing no letter of the first_word
    """
    first_word_letters = set(first_word)
    for word, score in scored_words.items():
        # making sure no duplicate letter in the word, and no duplicate letter between the first and second word
        if len(set(word)) == wordLength and not first_word_letters.intersection(set(word)):
            return (word, score)

def saveTopPairsTOCSV(top_pairs: list, filename: str) -> None:
    """
    Save the top pairs to a CSV file
    """
    with open(filename, "w") as f:
        headerList = ["First Word", "Second Word", "First Word Score", "Second Word Score", "Combined Score"]
        df = pd.DataFrame(top_pairs, columns=headerList)
        df.to_csv(f, index=False)


first_word_choices = getPossibleFirstWords(word_scores)
# print(first_word_choices)
first_word_scores = [word_scores[word] for word in first_word_choices]

"""
Create firstword-secondword word pairs with max info gain(score)
"""
# word_pair_choices = []
# for first_word, first_word_score in zip(first_word_choices, first_word_scores):
#     second_word, second_word_score = findSecondWord(first_word, word_scores)
#     # print(f"The second word is {second_word}")
#     word_pair_choices.append((first_word, second_word, first_word_score, second_word_score, first_word_score + second_word_score))

# # sort the word pairs by 4th element (first_word_score + second_word_score)
# word_pair_choices = sorted(word_pair_choices, key=lambda item: item[4], reverse=True)
# for entry in word_pair_choices:
#     print(f"{entry[0]} - {entry[1]} - {entry[2]:.2f} - {entry[3]:.2f} - {entry[4]:.2f}")


# save top 50 pairs to a CSV file
# saveTopPairsTOCSV(word_pair_choices[:50], "top_word_pairs.csv")

"""
Possible first two words are TALES and CORNY
or maybe, TONES and PARLY
or maybe, CONES and PARTY
"""
