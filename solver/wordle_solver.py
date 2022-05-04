import sys

sys.path.append('../helper')
sys.path.append('../scorer')
from wordle_helper import WordleHelper
from wordle_scorer import WordleScorer

def createVerdict(guessWord, answerWord) -> str:
    """
    Creates a verdict string by matching the guessed and answer word
    """
    # create a dict of all letters of answerWord with the frequency of letters
    # used to handle letters appearing more times in guessWord than in answerWord
    # example case: answerWord = "bored", guessWord = "boron"
    answerWordFreq = {letter: answerWord.count(letter) for letter in answerWord}

    verdict = ""
    for i in range(len(answerWord)):
        if guessWord[i] == answerWord[i]:
            verdict += '+'
            answerWordFreq[guessWord[i]] -= 1
        elif guessWord[i] in answerWord and answerWordFreq[guessWord[i]] > 0:
            verdict += '?'
            answerWordFreq[guessWord[i]] -= 1
        else:
            verdict += '-'
    return verdict

class WordleSolver:
    def __init__(self) -> None:
        self.maxNumberOfAttempts = 6
        self.wordlLength = 5
        self.positionalLetters = [None] * self.wordlLength
        self.existingLetters = ""
        self.possibleLetters = "qwertyuiopasdfghjklzxcvbnm"
        self.notPositionalLetters = [[] for _ in range(self.wordlLength)]
        self.dictionaryMode = False
        self.firstWord = "tales"
        self.secondWord = "corny"

    def __str__(self):
        # print posinalletters, existingLetters, possibleLetters, notPositionalLetters
        return "positionalLetters: {}\nexistingLetters: {}\npossibleLetters: {}\nnotPositionalLetters: {}".format(self.positionalLetters, self.existingLetters, self.possibleLetters, self.notPositionalLetters)

    def updateParamas(self, word: str, verdict: str) -> None:
        """ 
        Update the params according to the verdict of given word 
        verdict is given as '-' or '+' or '?' 
        '-' means the letter is absent in the word 
        '+' means the letter is in exact position 
        '?' means the letter is in the word but not in the exact position 
        : param word: the word to be checked 
        : param verdict: the verdict of the each letter of the word 
        """ 
        print(word, verdict)
        for i in range(self.wordlLength):
            if verdict[i] == '-':
                self.possibleLetters = self.possibleLetters.replace(word[i], "")
            elif verdict[i] == '+':
                self.positionalLetters[i] = word[i]
                self.possibleLetters = self.possibleLetters.replace(word[i], "")
            elif verdict[i] == '?':
                self.existingLetters += word[i]
                self.notPositionalLetters[i].append(word[i])

    def getHelpFromHelper(self) -> list:
        """
        Takes help from the wordle helper
        :return : a list of possible words 
        """
        helper = WordleHelper(self.positionalLetters, self.existingLetters, self.wordlLength, self.possibleLetters, self.notPositionalLetters, self.dictionaryMode)
        
        allValidWords = helper.getAllWords()
        print(len(allValidWords))
        return allValidWords

    def __giveFinalVerdict(self, attemptsTaken, foundAnswer, answerWord):
        if foundAnswer:
            print("The answer is {}".format(answerWord))
        else:
            print("The answer is not found, correct answer is {}".format(answerWord))
        print("Number of attempts taken: {}".format(attemptsTaken))

    def analyzeFixedGuess(self, attemptsTaken, guessWord, answerWord) -> bool: 
        """
        Analyzes a fixed guess word against the answer word
        : param guessWord: the guess word
        : param answerWord: the answer word
        """
        foundAnswer = guessWord == answerWord
        if foundAnswer:
            self.__giveFinalVerdict(attemptsTaken, foundAnswer, answerWord)
            return foundAnswer
        guessWordVerdict = createVerdict(guessWord, answerWord)
        self.updateParamas(guessWord, guessWordVerdict)
        return foundAnswer
        

    def solve(self, answerWord):
        """
        : param answerWord: the answer word
        : return: a list of all possible words
        """
        guessesTaken = set()
        attemptsTaken = 0
        # start with a fixed first word 
        attemptsTaken += 1
        foundAnswer = self.analyzeFixedGuess(attemptsTaken, self.firstWord, answerWord)
        guessesTaken.add(self.firstWord)
        if foundAnswer:
            return
        # print(self)
        # start with a fixed second word
        attemptsTaken += 1
        foundAnswer = self.analyzeFixedGuess(attemptsTaken, self.secondWord, answerWord)
        guessesTaken.add(self.secondWord)
        if foundAnswer:
            return
        # print(self)
        # now start exploring using scorer and helper
        while attemptsTaken < self.maxNumberOfAttempts:
            attemptsTaken += 1
            allValidWords = self.getHelpFromHelper()
            scorer = WordleScorer(allValidWords)
            wordScores = scorer.scoreAllWords()
            print(wordScores)
            # get the best word
            bestWord = max(wordScores, key = lambda k : wordScores[k])
            # if the best word is already guessed, try second best word
            while bestWord in guessesTaken:
                # remove bestWord from wordScores dict
                del wordScores[bestWord]
                print(wordScores)
                bestWord = max(wordScores, key = lambda k : wordScores[k])
            foundAnswer = bestWord == answerWord
            guessesTaken.add(bestWord)
            if foundAnswer:
                break
            print("Best word is {}".format(bestWord))
            bestWordVerdict = createVerdict(bestWord, answerWord)
            self.updateParamas(bestWord, bestWordVerdict)
            print(self)
        self.__giveFinalVerdict(attemptsTaken, foundAnswer, answerWord)

# test createVerdict
# print(createVerdict("bqroo", "bored"))


answerWord = "shout"
solver = WordleSolver()
solver.solve(answerWord)







