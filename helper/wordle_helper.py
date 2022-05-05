from tabnanny import verbose
from dictionary_api import DictionaryAPI
from typing import Union

allWordsSorted = open("../helper/allFiveLetterWords.txt").read().splitlines()
def existsInWordList(word):
    """
    Check whether the word exists in sorted allFiveLetterWords list
    """
    word = word.lower()
    lo = 0
    hi = len(allWordsSorted) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if allWordsSorted[mid] == word:
            return True
        elif allWordsSorted[mid] < word:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

def isMeaningfulWord(word: str, verbose = True) -> bool:
    """
    check if the word is Meaningful using DictionaryAPI
    :param word: word to check
    :param verbose: print out the result (default: True)
    :return: True if the word is found in DictionaryAPI, False otherwise
    """
    myDict = DictionaryAPI()
    wordMeaning = myDict.find_meaning(word)
    if not wordMeaning:
        return False
    if verbose:
        print("\n" + word.upper())
        for meaning in wordMeaning:
            if type(meaning) == dict:
                for key in meaning:
                    print(f"{key}: {meaning[key]}")
    return True
    
class WordleHelper:
    def __init__(self, positionalLetters: list, exisitingLetters: str, wordLength: int, possibleLetters: str, notPositionalLetters: list, dictionaryMode: bool = True):
        self.allPossibleWords = []
        self.meaningfulWords = []
        self.meaningNotFoundWords = []
        self.listedWords = []
        self.positionalLetters = positionalLetters
        self.myWordAsDict = self.__buildDictFromWord(positionalLetters)
        self.existingLetters = exisitingLetters
        self.wordLength = wordLength
        self.possibleLetters = possibleLetters
        self.backtrackCount = 0
        self.notPositionalLetters = notPositionalLetters
        self.dictionaryMode = dictionaryMode

    def __buildDictFromWord(self, letters: Union[list, str]) -> dict:
        """
        Returns a dictionary of index to letters
        """
        return {i: letters[i] for i in range(len(letters))}

    def __buildWordFromDict(self, wordAsDict: dict) -> str:
        """
        Build a word from myWord dict
        """
        word = ""
        for i in wordAsDict:
            # check if the letter is alphabetical
            if not wordAsDict[i]:
                return None
            word += wordAsDict[i]
        return word

    def __addWordToLists(self, word: str):
        """
        add the word to the both the lists(allPossibleWords, meaningfulWords, meaningNotFOundWords)
        """
        self.allPossibleWords.append(word)
        if existsInWordList(word):
            # print(word)
            self.listedWords.append(word)

    def __backtrackAllWords(self, idx: int, wordAsDict: Union[dict , str]):
        """
        backtrack to generate all the words from probableLetters
        """
        self.backtrackCount += 1
        if idx == 0:
            word = self.__buildWordFromDict(wordAsDict)
            if word:
                # check if word contains all the letters in self.existingLetters
                if all(letter in word for letter in self.existingLetters):
                    self.__addWordToLists(word)
            return
        for letter in self.probableLetters:
            # check if the letter is not in that position
            if letter in self.notPositionalLetters[idx-1]:
                continue
            # check if a letter already exists in that position
            if wordAsDict[idx-1] is not None:
                self.__backtrackAllWords(idx - 1, wordAsDict)
                return
            wordAsDict[idx-1] = letter
            self.__backtrackAllWords(idx - 1, wordAsDict)
            wordAsDict[idx-1] = None

    def __generateMeaningfulWords(self):
        """
        generate the meaningful words
        """
        for word in self.listedWords:
            if isMeaningfulWord(word, verbose = True):
                self.meaningfulWords.append(word.upper())
                if verbose:
                    print(f"{word} is a meaningful word")
            else:
                self.meaningNotFoundWords.append(word.upper())
                if verbose:
                    print(f"{word} is not a meaningful word")

    def buildAllWords(self):
        """
        build all the words by calling backtrackAllWords
        """
        self.lettersInCorrectPos = "".join(letter for letter in self.positionalLetters if letter)
        # add already correct letters into consideration to handle duplicates
        self.probableLetters = self.possibleLetters + self.lettersInCorrectPos
        self.__backtrackAllWords(self.wordLength, self.myWordAsDict)
    
    def printAllWords(self):
        """
        print all the words
        """
        print(f"\nNumber of all possible words : {len(self.allPossibleWords)}")
        if self.dictionaryMode:    
            self.__generateMeaningfulWords()
            print(f"\nMeaningful words found in dictionaryAPI: \n{self.meaningfulWords}")
            print(f"\nMeaningful word, but not in api (or down): {self.meaningNotFoundWords}\n")    
        else:
            print(f"\nAll valid 5 letter words: \n{self.listedWords}")
    
    def getAllWords(self):
        """
        return all the possible words
        """
        self.buildAllWords()
        return self.listedWords

if __name__ == '__main__':
    positionalLetters = [None, None, None, None, None]    # green letters
    existingLetters = 'boer'   # yellow letters
    wordLength = 5
    possibleLetters = 'qwypfjzxcvm' + existingLetters    # all letters - (grey letters + green letters)
    notPositionalLetters = [['b', 'r'], ['o', 'e'], [], ['r', 'e'], []]
    # positionalLetters = ['s', None, None, None, None]    # green letters
    # existingLetters = 'l'   # yellow letters
    # wordLength = 5
    # possibleLetters = 'qweyuazxn'
    # notPositionalLetters = [[], [], [], [], []]
    dictionaryMode = False

    wordleHelper = WordleHelper(positionalLetters, existingLetters, wordLength, possibleLetters, notPositionalLetters, dictionaryMode)
    wordleHelper.buildAllWords()
    wordleHelper.printAllWords()
    