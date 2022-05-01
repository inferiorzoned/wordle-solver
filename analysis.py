# take all words from allFiveLetterWords.txt and create a frequency table of all possitional letters
import csv
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


def saveFreqWeights(freq: np.array, filename: str) -> None:
    """
    Save the frequency weights to a file
    """
    with open(filename, "w") as f:
        f.write("5 positions with the probablity of each letter\n")
        for i in range(wordLength):
            for j in range(numberOfLetters):
                f.write(f"{chr(ord('A') + j)} : {freq_weights[i][j]:.1f}")
                if j != numberOfLetters - 1:
                    f.write(", ")
            f.write("\n")

        f.write(
            "\n26 letters with the weighted frequency of being in 5 positions\n"
        )
        for j in range(numberOfLetters):
            for i in range(wordLength):
                f.write(f"{chr(ord('A') + j)} : {freq_weights[i][j]:.1f}")
                if i != wordLength - 1:
                    f.write(", ")
            f.write("\n")

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


def calculateScore(word: str, freq: np.array) -> float:
    """
    Calculate the score of a word using the frequency table
    """
    score = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 2wordLength
        letter = ord(letter) - ord('a')
        # increment the score
        score += freq[idx][letter]
    return score


def saveWordScores(word_scores: dict, filename: str) -> None:
    # save all word scores to a file
    with open(filename, "w") as f:
        for word, score in word_scores.items():
            f.write(f"{word} - {score}\n")

def findSecondWord(first_word: str, scored_words: tuple) -> tuple:
    """
    Return the (word, score) with the highest score containing no letter of the first_word
    """
    first_word_letters = set(first_word)
    for word, score in scored_words.items():
        if not first_word_letters.intersection(set(word)):
            return (word, score)

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

allWordsSorted = open("allFiveLetterWords.txt").read().splitlines()
freq = createFrequencyTable(allWordsSorted)
# count frequeuncy table to weighted frequency table
freq_weights = (freq / freq.sum(axis=1, keepdims=True)) * 100
saveLetterFreqWeightsCSV(freq_weights, "weighted_freqs_letters_positions.csv")

# print(freq_weights)
# print(freq)
saveFreqWeights(freq_weights, "possionalLetterWeights.txt")
# create a dict of words from allWordsSorted with scores as values
word_scores = dict(map(lambda w: (w, calculateScore(w, freq_weights)), allWordsSorted))
word_scores = {k: v for k, v in sorted(word_scores.items(), key=lambda item: item[1], reverse=True)}

saveWordScores(word_scores, "allWordsScores.txt")


"""
Starting first two words analysis
"""
first_word_choices = [
    "cares", "bares", "pares", "tares", "cores", "bores", "mares", "pores",
    "canes", "dares", "banes", "tores", "gares", "panes", "fares", "lares",
    "bales", "mores", "cones", "dores", "pales", "bones", "saxes", "hares", "gores", "tales", "manes"
]
first_word_scores = [word_scores[word] for word in first_word_choices]

word_pair_choices = []
# print(first_word_scores)
for first_word, first_word_score in zip(first_word_choices, first_word_scores):
    second_word, second_word_score = findSecondWord(first_word, word_scores)
    # print(f"The second word is {second_word}")
    word_pair_choices.append((first_word, second_word, first_word_score, second_word_score, first_word_score + second_word_score))

for entry in word_pair_choices:
    print(f"{entry[0]} - {entry[1]} - {entry[2]:.2f} - {entry[3]:.2f} - {entry[4]:.2f}")

"""
Possible first two words are CANES and BORTY
or maybe, TALES and CORNY
"""

letterWeights =  getLetterSummedWeights(freq_weights)
print(letterWeights)
saveLetterTotalWeightsCSV(letterWeights, "letterTotalWeights.csv")
lettersWeightsSorted = {k:v for k, v in sorted(letterWeights.items(), key=lambda item: item[1], reverse=True)}
print(lettersWeightsSorted)