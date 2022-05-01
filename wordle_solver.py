from wordle_helper import WordleHelper
from scorer.wordle_scorer import WordleScorer

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
        self.wordlLength = 5
        self.positionalLetters = [None] * self.wordlLength
        self.existingLetters = ""
        self.possibleLetters = "qwertyuiopasdfghjklzxcvbnm"
        self.notPositionalLetters = [[]] * self.wordlLength

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
        # letterToVerdict = {(word[i], verdict[i]) for i in range(self.wordLength)}
        for i in range(self.wordlLength):
            if verdict[i] == '-':
                self.possibleLetters.replace(word[i], "")
            elif verdict[i] == '+':
                self.positionalLetters[i] = word[i]
            elif verdict[i] == '?':
                self.existingLetters += word[i]
                self.notPositionalLetters[i].append(word[i])

    def getHelpFromHelper(self) -> list:
        """
        Takes help from the wordle helper
        :return : a list of possible words 
        """
        helper = WordleHelper(self.positionalLetters, self.existingLetters, self.wordlLength, self.possibleLetters, self.notPositionalLetters)
        
        allValidWords = helper.getAllWords()
        print(len(allValidWords))
        return allValidWords

    def solve(self, answerWord):
        """
        : param answerWord: the answer word
        : return: a list of all possible words
        """
        # start with a chosen first word 
        firstWord = "tales"
        firstWordVerdict = createVerdict(firstWord, answerWord)
        self.updateParamas(firstWord, firstWordVerdict)
        # start with a chosen second word
        secondWord = "corny"
        secondWordVerdict = createVerdict(secondWord, answerWord)
        self.updateParamas(secondWord, secondWordVerdict)
        # now start exploring using scorer and helper
        allValidWords = self.getHelpFromHelper()
        scorer = WordleScorer(allValidWords)
        wordScores = scorer.scoreAllWords()
        print(wordScores)


    def scoreWords(self, allValidWords: list) -> dict:
        """
        : param allValidWords: 
        """
        pass    


# test createVerdict
# print(createVerdict("bqroo", "bored"))


answerWord = "brain"
solver = WordleSolver()
solver.solve(answerWord)







