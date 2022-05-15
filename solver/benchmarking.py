from wordle_solver import WordleSolver
from config import Config
import csv
from tqdm import tqdm

allWordleWords = open("included.txt").read().splitlines()

def singleWordPairAnalysis(saveToFile = False):
    wordAttemptDict = {}
    attemptCount = 0
    attemptSum = 0
    guessedWithinAllowedAttempts = 0
    for word in tqdm(allWordleWords):
        solver = WordleSolver()
        solver.testSolver(word)
        wordAttemptDict[word] = solver.attemptsTaken
        attemptSum += solver.attemptsTaken
        attemptCount += 1
        if solver.attemptsTaken <= Config.allowedNumberOfAttempts:
            guessedWithinAllowedAttempts += 1
        else:
            print(f"{attemptCount - guessedWithinAllowedAttempts} words could not be guessed")
            print(f"{word} took {solver.attemptsTaken} attempts")
    print(wordAttemptDict)
    print(f"Total number of attempts are {attemptSum}")
    print(f"Number of wordle words are {attemptCount}")
    print(f"Average attempt is {attemptSum/attemptCount}")
    print(f"Number of words guessed within {Config.allowedNumberOfAttempts} attempts is {guessedWithinAllowedAttempts}")

def loadWordPairs(filename: str) -> list:
    """
    Load the word pairs from a file
    """
    word_pairs = []
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=',')
        # skip the header
        next(reader)
        for row in reader:
            word_pairs.append((row[0], row[1]))
    return word_pairs

def allWordPairAnalysis():
    # load all word pairs (top 50)
    word_pairs = loadWordPairs("word_pair_analysis/top_word_pairs.csv")
    for firstWord, secondWord in word_pairs:
        Config.firstWord = firstWord
        Config.secondWord = secondWord
        singleWordPairAnalysis(saveToFile = True)


# analyze with the word pair from the config file
singleWordPairAnalysis()

# analyze with all word pairs
# allWordPairAnalysis()