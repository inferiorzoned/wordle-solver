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
        






