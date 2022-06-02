from tabnanny import verbose
from dictionary_api import DictionaryAPI
from typing import Union

# allWordsSorted = open("../helper/allFiveLetterWords.txt").read().splitlines()
allWordsSorted = open("../helper/allWordleWords.txt").read().splitlines()

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
        self.myWordAsDict = self.buildDictFromWord(positionalLetters)
        self.existingLetters = exisitingLetters
        self.wordLength = wordLength
        self.possibleLetters = possibleLetters
        self.backtrackCount = 0
        self.notPositionalLetters = notPositionalLetters
        self.dictionaryMode = dictionaryMode

    def buildDictFromWord(self, letters: Union[list, str]) -> dict:
        """
        Returns a dictionary of index to letters
        : return: the dictionary
        """
        return {i: letters[i] for i in range(len(letters))}

    def buildWordFromDict(self, wordAsDict: dict) -> str:
        """
        Build a word from myWord dict
        :param wordAsDict: the dictionary of index to letters
        :return: the word
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
        : param word: the word to add
        """
        self.allPossibleWords.append(word)
        if existsInWordList(word):
            # print(word)
            self.listedWords.append(word)

    def __backtrackAllWords(self, idx: int, wordAsDict: Union[dict , str]):
        """
        backtrack to generate all the words from probableLetters
        :param idx: the index to check
        :param wordAsDict: the dictionary of index to letters
        """
        self.backtrackCount += 1
        if idx == 0:
            word = self.buildWordFromDict(wordAsDict)
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

    def __addWordsFromWordlist(self):
        """
        add words listedwords from the word list based on the criterias
        """
        for word in allWordsSorted:
            # check if word contains only the letters from self.probableLetters
            if not all(letter in self.probableLetters for letter in word):
                continue
            # check if word contains the positional letters at the correct position
            containsPositionalLetters = True
            for i in range(self.wordLength):
                if self.positionalLetters[i] :
                    if word[i] != self.positionalLetters[i]:
                        containsPositionalLetters = False
                        break
            if not containsPositionalLetters:
                continue
            # check if word does not contain any of the notPositionalLetters at correct position
            containsNotPositionalLetters = False
            for i in range(self.wordLength):
                if self.notPositionalLetters[i] :
                    if word[i] in self.notPositionalLetters[i]:
                        containsNotPositionalLetters = True
                        break
            if containsNotPositionalLetters:
                continue
            # check if word contains all the letters in self.existingLetters
            if all(letter in word for letter in self.existingLetters):
                self.listedWords.append(word)
            

    def buildAllWords(self):
        """
        build all the words by calling backtrackAllWords
        """
        self.lettersInCorrectPos = "".join(letter for letter in self.positionalLetters if letter)
        # add already correct letters into consideration to handle duplicates
        self.probableLetters = self.possibleLetters + self.existingLetters + self.lettersInCorrectPos 
        # self.__backtrackAllWords(self.wordLength, self.myWordAsDict)
        self.__addWordsFromWordlist()
    
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
        :return: wordlist
        """
        self.buildAllWords()
        return self.listedWords

if __name__ == '__main__':
    # positionalLetters = [None, None, None, None, None]    # green letters
    # existingLetters = 'boer'   # yellow letters
    # wordLength = 5
    # possibleLetters = 'qwypfjzxcvm' + existingLetters    # all letters - (grey letters + green letters)
    # notPositionalLetters = [['b', 'r'], ['o', 'e'], [], ['r', 'e'], []]
    positionalLetters = [None, 'i', None, None, 'y']    # green letters
    existingLetters = 'id'   # yellow letters
    wordLength = 5
    possibleLetters = 'qwpfgjkzxv'   # all letters - (grey letters + green letters + yellow letters)
    notPositionalLetters = [['t', 'c', 'h', 'b'], ['a', 'o', 'u'], ['l', 'r', 'm', 'd'], ['e', 'n', 'i', 'd'], ['s', 'd']]
    dictionaryMode = False

    wordleHelper = WordleHelper(positionalLetters, existingLetters, wordLength, possibleLetters, notPositionalLetters, dictionaryMode)
    wordleHelper.buildAllWords()
    wordleHelper.printAllWords()
    