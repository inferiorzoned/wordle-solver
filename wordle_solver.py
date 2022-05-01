from wordle_helper import WordleHelper

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
        wordleHelper = WordleHelper(self.positionalLetters, self.existingLetters, self.wordlLength, self.possibleLetters, self.notPositionalLetters)
        allValidWords = wordleHelper.getAllWords()

    def scoreWords(self, allValidWords: list) -> dict:
        """
        : param allValidWords: 
        """
        pass    

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
        print(answerWordFreq)
        if guessWord[i] == answerWord[i]:
            verdict += '+'
            answerWordFreq[guessWord[i]] -= 1
        elif guessWord[i] in answerWord and answerWordFreq[guessWord[i]] > 0:
            verdict += '?'
            answerWordFreq[guessWord[i]] -= 1
        else:
            verdict += '-'
    return verdict

# test createVerdict
print(createVerdict("bqroo", "bored"))
    
        






