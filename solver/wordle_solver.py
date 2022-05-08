from distutils.log import info
from re import S
import sys

sys.path.append('../helper')
sys.path.append('../scorer')
from wordle_helper import WordleHelper
from wordle_scorer import WordleScorer, precalculateScores
from config import Config

def createVerdict(guessWord, answerWord) -> str:
    """
    Creates a verdict string by matching the guessed and answer word
    : param guessWord: the guessed word
    : param answerWord: the answer word
    : return: a verdict string
    """
    # create a dict of all letters of answerWord and guessWord with the frequency of letters
    # used to handle letters appearing more times in guessWord than in answerWord
    # example case: guessWord="boron", answerWord="bored"; guessWord="roper", answerWord="homer"
    answerWordFreq = {letter: answerWord.count(letter) for letter in answerWord}
    guessWordFreq = {letter: guessWord.count(letter) for letter in guessWord}
    if Config.debugMode > 1:
        print("answerWord", answerWord, answerWordFreq)
        print("guessWord ", guessWord, guessWordFreq)

    verdict = ""
    for i in range(len(answerWord)):
        if guessWord[i] == answerWord[i]:
            verdict += '+'
        elif guessWord[i] in answerWord:
            if answerWordFreq[guessWord[i]] >= guessWordFreq[guessWord[i]]:
                verdict += '?'
            else:
                verdict += '-'
                guessWordFreq[guessWord[i]] -= 1
        else:
            verdict += '-'
    return verdict

class WordleSolver:
    def __init__(self) -> None:
        self.positionalLetters = [None] * Config.wordLength 
        self.existingLetters = ""
        self.possibleLetters = "qwertyuiopasdfghjklzxcvbnm"
        self.notPositionalLetters = [[] for _ in range(Config.wordLength )]
        self.dictionaryMode = False
        self.attemptsTaken = 0
        self.infoGainAtSecondAttempt = False
        self.infoGainAtThirdAttempt = False
        precalculateScores()


    def __str__(self):
        """
        : return posinalletters, existingLetters, possibleLetters, notPositionalLetters
        """
        return "positionalLetters: {}\nexistingLetters: {}\npossibleLetters: {}\nnotPositionalLetters: {}".format(self.positionalLetters, self.existingLetters, self.possibleLetters, self.notPositionalLetters)

    def updateParams(self, word: str, verdict: str) -> None:
        """ 
        Update the params according to the verdict of given word 
        verdict is given as '-' or '+' or '?' 
        '-' means the letter is absent in the word 
        '+' means the letter is in exact position 
        '?' means the letter is in the word but not in the exact position 
        : param word: the word to be checked 
        : param verdict: the verdict of the each letter of the word 
        """ 
        if Config.debugMode > 0:
            print(word, verdict)  
        for i in range(Config.wordLength ):
            if verdict[i] == '-':
                self.possibleLetters = self.possibleLetters.replace(word[i], "")
                self.notPositionalLetters[i].append(word[i])
            elif verdict[i] == '+':
                self.positionalLetters[i] = word[i]
                self.existingLetters = self.existingLetters.replace(word[i], "")
                self.possibleLetters = self.possibleLetters.replace(word[i], "")
            elif verdict[i] == '?':
                if word[i] not in self.existingLetters:
                    self.existingLetters += word[i]
                self.notPositionalLetters[i].append(word[i])
                self.possibleLetters = self.possibleLetters.replace(word[i], "")
                

    def __getHelpFromHelper(self) -> list:
        """
        Takes help from the wordle helper
        :return : a list of possible words 
        """
        helper = WordleHelper(self.positionalLetters, self.existingLetters, Config.wordLength , self.possibleLetters, self.notPositionalLetters, self.dictionaryMode)
        
        allValidWords = helper.getAllWords()
        print(f"Number of words found: {len(allValidWords)}")
        return allValidWords

    def scoreTheWords(self, wordlist) -> dict:
        """
        Scores the words in the wordlist
        : param wordlist: the list of words to be scored
        : return: a list of scores for each word in the wordlist
        """
        scorer = WordleScorer(wordlist)
        return scorer.scoreAllWords()
    
    def __getBestwordWithoutDuplicates(self, previousBestWord: str, wordScores: dict = None) -> str:
        """
        Gets the best word from the wordlist without duplicates
        : param wordScores: the scores of the words in the wordlist
        : param previousBestWord: the best word found so far
        : return: the best word without duplicates
        """
        bestWord = previousBestWord
        while (len(set(bestWord)) < Config.wordLength):
            del wordScores[bestWord]
            if len(wordScores) == 0:
                return previousBestWord
            bestWord = max(wordScores, key = lambda k : wordScores[k])
        return bestWord

    def getBestIfAlreadyGuessed(self, previousBestWord: str, wordScores: dict) -> str:
        """
        if the best word is already guessed, return the next best word
        : param previousBestWord: the best word found so far
        : param wordScores: the scores of the words in the wordlist
        : return: the best word
        """
        bestWord = previousBestWord
        while bestWord in self.guessesTaken:
            del wordScores[bestWord]
            bestWord = max(wordScores, key = lambda k : wordScores[k])
            if Config.debugMode > 0:
                print(wordScores)
                print(f"Best word: {bestWord.upper()} in attempt no {self.attemptsTaken}")
        return bestWord

    def __getInfoGainedBestword(self, previousBestWord: str = None, wordScores: dict = None) -> str:
        """
        Gets the best word by gaining info in different attempts
        : param wordScores: the scores of the words in the wordlist
        : param previousBestWord: the best word found so far
        : return: the best word with info gained
        """
        bestWord = previousBestWord
        # in 2nd attempt, try to discard all green letters (if any)
        if self.attemptsTaken == 2 and not self.infoGainAtSecondAttempt:
            temp = self.positionalLetters
            self.positionalLetters = [None] * Config.wordLength
            if Config.debugMode > 0:
                print(self)
            self.infoGainAtSecondAttempt = True
            bestWord = self.__getBestWord()
            self.positionalLetters = temp
            return bestWord
        # In 3rd attempt, if there are more than 10 words in wordScores, 
        # try to discard all green letters (if any exists)
        # and search for the best word again (to gain more info)
        if self.attemptsTaken == 3 and len(wordScores) >= 10 and any(self.positionalLetters) and not self.infoGainAtThirdAttempt:
            temp = self.positionalLetters
            self.positionalLetters = [None] * Config.wordLength 
            if Config.debugMode > 0:
                print(self)
            self.infoGainAtThirdAttempt = True
            # bestWord = self.__getBestWord() or bestWord
            allValidWords = self.__getHelpFromHelper()
            if len(allValidWords) > 0:
                wordScores = self.scoreTheWords(allValidWords)
                bestWord = max(wordScores, key = lambda k : wordScores[k])
                if Config.debugMode > 0:
                    print(wordScores)
                    print(f"Best word is {bestWord.upper()} in attempt no {self.attemptsTaken}")
                bestWord = self.getBestIfAlreadyGuessed(bestWord, wordScores)
                bestWord = self.__getBestwordWithoutDuplicates(bestWord, wordScores)
            self.positionalLetters = temp
            return bestWord
        # if attempts taken is less than 4, try not to include duplicates
        if self.attemptsTaken <= 4:
            bestWord = self.__getBestwordWithoutDuplicates(bestWord, wordScores)
            print(f"Best word: {bestWord.upper()} in attempt no {self.attemptsTaken}")
        return bestWord

    def __getBestWord(self) -> str:
        """
        Returns the best word from the given word scores
        """
        if self.attemptsTaken == 2 and not self.infoGainAtSecondAttempt:
            return self.__getInfoGainedBestword()
        allValidWords = self.__getHelpFromHelper()
        if len(allValidWords) == 0:
            return None
        wordScores = self.scoreTheWords(allValidWords)
        bestWord = max(wordScores, key = lambda k : wordScores[k])
        if Config.debugMode > 0:
            print(wordScores)
            print(f"Best word is {bestWord.upper()} in attempt no {self.attemptsTaken}")
        # if the best word is already guessed, get the next best word
        bestWord = self.getBestIfAlreadyGuessed(bestWord, wordScores)
        # get the best word with additional info gained
        bestWord = self.__getInfoGainedBestword(bestWord, wordScores)
        return bestWord

    def __giveFinalVerdict(self, foundAnswer, answerWord):
        """
        Give the final verdict of the game
        : param foundAnswer: the word found
        : param answerWord: the answer word
        """
        if foundAnswer and self.attemptsTaken <= Config.allowedNumberOfAttempts:
            print(f"The correct answer is {answerWord}, number of attempts taken: {self.attemptsTaken}")
        else:
            print("The answer is not found, correct answer is {}".format(answerWord))
            print(f"Number of attempts taken: {self.attemptsTaken}")

    def analyzeFixedGuess(self, guessWord, answerWord) -> bool: 
        """
        Analyzes a fixed guess word against the answer word
        : param guessWord: the guess word
        : param answerWord: the answer word
        """
        foundAnswer = guessWord == answerWord
        if foundAnswer:
            self.__giveFinalVerdict(foundAnswer, answerWord)
            return foundAnswer
        guessWordVerdict = createVerdict(guessWord, answerWord)
        self.updateParams(guessWord, guessWordVerdict)
        return foundAnswer

    def testSolver(self, answerWord):
        """
        : param answerWord: the answer word
        """
        self.guessesTaken = set()
        self.attemptsTaken = 0
        # start with a fixed first word 
        self.attemptsTaken += 1
        if Config.debugMode > 0:
            print(f"Attempt no {self.attemptsTaken}")
        foundAnswer = self.analyzeFixedGuess(Config.firstWord, answerWord)
        self.guessesTaken.add(Config.firstWord)
        if foundAnswer:
            return
        if Config.debugMode > 0:
            print(self)
        # start with a fixed second word
        # self.attemptsTaken += 1
        # if Config.debugMode > 0:
        #     print(f"Attempt no {self.attemptsTaken}")
        # foundAnswer = self.analyzeFixedGuess(Config.secondWord, answerWord)
        # self.guessesTaken.add(Config.secondWord)
        # if foundAnswer:
        #     return
        # if Config.debugMode > 0:
        #     print(self)
        while self.attemptsTaken < Config.maxNumberOfAttempts:
            self.attemptsTaken += 1
            if Config.debugMode > 0:
                print(f"Attempt no {self.attemptsTaken}")
            bestWord = self.__getBestWord()
            foundAnswer = bestWord == answerWord
            self.guessesTaken.add(bestWord)
            if foundAnswer:
                break
            print(f"Best word: {bestWord.upper()} in attempt no {self.attemptsTaken}")
            bestWordVerdict = createVerdict(bestWord, answerWord)
            self.updateParams(bestWord, bestWordVerdict)
            if Config.debugMode > 0:
                print(self)
        self.__giveFinalVerdict(foundAnswer, answerWord)

    def getNextGuess(self):
        """
        Returns the next word to be guessed
        """
        self.attemptsTaken += 1
        self.guessesTaken = set()
        if self.attemptsTaken == 1:
            self.guessesTaken.add(Config.firstWord)
            return Config.firstWord
        elif self.attemptsTaken == 2:
            self.guessesTaken.add(Config.secondWord)
            return Config.secondWord
        bestWord = self.__getBestWord()
        self.guessesTaken.add(bestWord)
        return bestWord

def runSolver(solver):
    while(True):
        myGuess = solver.getNextGuess()
        print(f"Best word is {myGuess.upper()} in attempt no {solver.attemptsTaken}")

        print("give the verdict for the guess")
        verdict = input()
        if verdict == "+++++":
            break
        solver.updateParams(myGuess, verdict)

    print("Number of attempts taken: {}".format(solver.attemptsTaken))


# test createVerdict
# print(createVerdict("tones", "robot"))

solver = WordleSolver()
"""
testing the solver# runSolver(solver)
"""
answerWord = "filer"
solver.testSolver(answerWord)

"""
running the solver
"""
# runSolver(solver)






