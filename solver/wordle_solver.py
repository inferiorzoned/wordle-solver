import sys

sys.path.append('../helper')
sys.path.append('../scorer')
from wordle_helper import WordleHelper
from wordle_scorer import WordleScorer
from config import Config

def createVerdict(guessWord, answerWord) -> str:
    """
    Creates a verdict string by matching the guessed and answer word
    """
    # create a dict of all letters of answerWord and guessWord with the frequency of letters
    # used to handle letters appearing more times in guessWord than in answerWord
    # example case: guessWord="boron", answerWord="bored"; guessWord="roper", answerWord="homer"
    answerWordFreq = {letter: answerWord.count(letter) for letter in answerWord}
    guessWordFreq = {letter: guessWord.count(letter) for letter in guessWord}
    # print("answerWord", answerWord, answerWordFreq)
    # print("guessWord ", guessWord, guessWordFreq)

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
        self.maxNumberOfAttempts = Config.maxNumberOfAttempts
        self.wordlLength = Config.wordLength
        self.positionalLetters = [None] * self.wordlLength
        self.existingLetters = ""
        self.possibleLetters = "qwertyuiopasdfghjklzxcvbnm"
        self.notPositionalLetters = [[] for _ in range(self.wordlLength)]
        self.dictionaryMode = False
        self.firstWord = Config.firstWord
        self.secondWord = Config.secondWord
        self.attemptsTaken = 0
        self.infoGainAtThirdAttempt = False

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
                self.notPositionalLetters[i].append(word[i])
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

    def scoreTheWords(self, wordlist) -> dict:
        """
        Scores the words in the wordlist
        : param wordlist: the list of words to be scored
        : return: a list of scores for each word in the wordlist
        """
        scorer = WordleScorer(wordlist)
        return scorer.scoreAllWords()
    
    def getBestwordWithoutDuplicates(self, wordScores: dict, previousBestWord: str) -> str:
        """
        Gets the best word from the wordlist without duplicates
        : param wordScores: the scores of the words in the wordlist
        : param previousBestWord: the best word found so far
        : return: the best word without duplicates
        """
        bestWord = previousBestWord
        while (len(set(bestWord)) < self.wordlLength):
            del wordScores[bestWord]
            if len(wordScores) == 0:
                return previousBestWord
            bestWord = max(wordScores, key = lambda k : wordScores[k])
        return bestWord

    def getBestWord(self) -> str:
        """
        Returns the best word from the given word scores
        : param wordScores: a dictionary of words and their scores
        """
        allValidWords = self.getHelpFromHelper()
        if len(allValidWords) == 0:
            return None
        wordScores = self.scoreTheWords(allValidWords)
        print(wordScores)
        bestWord = max(wordScores, key = lambda k : wordScores[k])
        # if the best word is already guessed, try second best word
        while bestWord in self.guessesTaken:
            # remove bestWord from wordScores dict
            del wordScores[bestWord]
            print(wordScores)
            bestWord = max(wordScores, key = lambda k : wordScores[k])
        """
        some info gaining tweaks
        """
        # In 3rd attempt, if there are more than 25 words in wordScores, try to discard all green letters (if any exists)
        if self.attemptsTaken <= 3 and len(wordScores) >= 25 and any(self.positionalLetters) and not self.infoGainAtThirdAttempt:
            temp = self.positionalLetters
            self.positionalLetters = [None] * self.wordlLength
            self.infoGainAtThirdAttempt = True
            bestWord = self.getBestWord() or bestWord
            self.positionalLetters = temp
        # if attempts taken is less than 4, try not to include duplicates
        if self.attemptsTaken <= 4:
            bestWord = self.getBestwordWithoutDuplicates(wordScores, bestWord)
        return bestWord

    def __giveFinalVerdict(self, foundAnswer, answerWord):
        if foundAnswer:
            print("The answer is {}".format(answerWord))
        else:
            print("The answer is not found, correct answer is {}".format(answerWord))
        print("Number of attempts taken: {}".format(self.attemptsTaken))

    def analyzeFixedGuess(self, guessWord, answerWord) -> bool: 
        """
        Analyzes a fixed guess word against the answer word
        : param guessWord: the guess word
        : param answerWord: the answer word
        """
        foundAnswer = guessWord == answerWord
        if foundAnswer:
            self.__giveFinalVerdict(self.attemptsTaken, foundAnswer, answerWord)
            return foundAnswer
        guessWordVerdict = createVerdict(guessWord, answerWord)
        self.updateParamas(guessWord, guessWordVerdict)
        return foundAnswer

    def testSolver(self, answerWord):
        """
        : param answerWord: the answer word
        : return: a list of all possible words
        """
        self.guessesTaken = set()
        self.attemptsTaken = 0
        # start with a fixed first word 
        self.attemptsTaken += 1
        foundAnswer = self.analyzeFixedGuess(self.firstWord, answerWord)
        self.guessesTaken.add(self.firstWord)
        if foundAnswer:
            return
        print(self)
        # start with a fixed second word
        self.attemptsTaken += 1
        foundAnswer = self.analyzeFixedGuess(self.secondWord, answerWord)
        self.guessesTaken.add(self.secondWord)
        if foundAnswer:
            return
        print(self)
        # now start exploring using scorer and helper
        while self.attemptsTaken < self.maxNumberOfAttempts:
            self.attemptsTaken += 1
            bestWord = self.getBestWord()
            foundAnswer = bestWord == answerWord
            self.guessesTaken.add(bestWord)
            if foundAnswer:
                break
            print(f"Best word is {bestWord.upper()} with {self.attemptsTaken} attempts")
            bestWordVerdict = createVerdict(bestWord, answerWord)
            self.updateParamas(bestWord, bestWordVerdict)
            print(self)
        self.__giveFinalVerdict(foundAnswer, answerWord)

    def getNextGuess(self):
        """
        Returns the next word to be guessed
        """
        self.attemptsTaken += 1
        self.guessesTaken = set()
        if self.attemptsTaken == 1:
            self.guessesTaken.add(self.firstWord)
            return self.firstWord
        elif self.attemptsTaken == 2:
            self.guessesTaken.add(self.secondWord)
            return self.secondWord
        bestWord = self.getBestWord()
        self.guessesTaken.add(bestWord)
        return bestWord


# test createVerdict
# print(createVerdict("rrrrr", "rooro"))

# answerWord = "inbox"
solver = WordleSolver()
# solver.testSolver(answerWord)

while(True):
    myGuess = solver.getNextGuess()
    print(f"Best word is {myGuess.upper()} with {solver.attemptsTaken} attempts")

    print("give the verdict for the guess")
    verdict = input()
    if verdict == "+++++":
        break
    solver.updateParamas(myGuess, verdict)

print("Number of attempts taken: {}".format(solver.attemptsTaken))









