# import enchant
# import pyttsx3
# from PyDictionary import PyDictionary

from dictionary_api import DictionaryAPI

class Speaking:
 
    def speak(self, audio):
       
        # Having the initial constructor of pyttsx3
        # and having the sapi5 in it as a parameter
        engine = pyttsx3.init('sapi5')
         
        # Calling the getter and setter of pyttsx3
        voices = engine.getProperty('voices')
         
        # Method for the speaking of the the assistant
        engine.setProperty('voice', voices[0].id)
        engine.say(audio)
        engine.runAndWait()

class wordle:
    def __init__(self, ache, probable):
        self.ache = ache
        self.probable = probable
        self.words = []
        

    
    def findWordSuffix(self):    #use this function when you know the suffix of the word
        # ache = 'ack'
        # probable = 'sacktypdfjzxm'

        for i in self.probable:
            for j in self.probable:
                print( i + j + self.ache)
                self.words.append( i + j + self.ache)
                
            print('\n')

    def findWordPrefix(self):    #use this function when you know the prefix of the word
        
        for i in self.probable:
            for j in self.probable:
                print(self.ache + i + j)
                self.words.append(self.ache + i + j)
            print('\n')

    def checkWordValidity(self):
        d1 = enchant.Dict("en_US")
        d2 = enchant.Dict("en_GB")

        speak = Speaking()
        dic = PyDictionary()
        speak.speak("Which word do u want to find the meaning of?")

        for i in self.words:
            if d1.check(i) == True:
                print(i, 'is a valid English word')

                meaning = dic.meaning(i)
                print(len(meaning))
         
                for state in meaning:
                    print(meaning[state])
                    speak.speak("the meaning  is" + str(meaning[state]))
            elif d2.check(i) == True:
                print(i, 'is a valid British word')
                
                meaning = dic.meaning(i)
                print(len(meaning))
         
                for state in meaning:
                    print(meaning[state])
                    speak.speak("the meaning  is" + str(meaning[state]))
        
        # Taking the string input
        
    def isValidWord(self, word: str, verbose = True) -> bool:
        """
        check if the word is valid using DictionaryAPI
        """
        myDict = DictionaryAPI()
        wordMeaning = myDict.find_meaning(word)
        if not wordMeaning:
            return False
        if verbose:
            print(word.upper())
            for meaning in wordMeaning:
                if type(meaning) == dict:
                    for key in meaning:
                        print(f"{key}: {meaning[key]}")
        return True
    

# this code works if exactly two letter is unknown :P

if __name__ == '__main__':
    ache = input('Enter the exact positional letters: ')
    probable = input('Enter the probable letters: ')
    wordle = wordle(ache, probable)
    wordle.findWordSuffix()
    # wordle.checkWordValidity()
    wordle.isValidWord("help")




        