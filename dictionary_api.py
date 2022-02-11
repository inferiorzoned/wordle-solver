import requests

# sample response to request to the api endpoint
'''
[
   {
      "word":"chaos",
      "phonetic":"ˈkeɪɒs",
      "phonetics":[
         {
            "text":"ˈkeɪɒs",
            "audio":"//ssl.gstatic.com/dictionary/static/sounds/20200429/chaos--_gb_1.mp3"
         }
      ],
      "origin":"late 15th century (denoting a gaping void or chasm, later formless primordial matter): via French and Latin from Greek khaos ‘vast chasm, void’.",
      "meanings":[
         {
            "partOfSpeech":"noun",
            "definitions":[
               {
                  "definition":"complete disorder and confusion.",
                  "example":"snow caused chaos in the region",
                  "synonyms":[
                     "disorder",
                     "disarray",
                     "disorganization",
                     "confusion",
                     "mayhem",
                     "bedlam",
                     "pandemonium",
                     "madness",
                     "havoc",
                     "turmoil",
                     "tumult",
                     "commotion",
                     "disruption",
                     "upheaval",
                     "furore",
                     "frenzy",
                     "uproar",
                     "hue and cry",
                     "babel",
                     "hurly-burly",
                     "a maelstrom",
                     "a muddle",
                     "a mess",
                     "a shambles",
                     "a mare's nest",
                     "anarchy",
                     "entropy",
                     "lawlessness",
                     "bangarang",
                     "hullabaloo",
                     "all hell broken loose",
                     "a madhouse",
                     "an omnishambles",
                     "a car crash",
                     "a three-ring circus"
                  ],
                  "antonyms":[
                     "order",
                     "orderliness"
                  ]
               }
            ]
         }
      ]
   }
]
'''

# def __get_items

class DictionaryAPI:
    def __init__(self):
        self.API_ENDPOINT = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    def __flatten_2d_list(self, list_2d: list) -> list:
        """
        Flattens a 2d list to a 1d list
        """
        return [item for sublist in list_2d for item in sublist]

    def __get_items(self, item_type: any, container: any) -> list:
        """
        Returns a list of items of type item_type from container
        """
        # check item_type is a key for all items in container, if not, create an empty item
        for item in container:
            if item_type not in item:
                item[item_type] = "N/A"
        return list(map(lambda item: item[str(item_type)] , container))

    def __add_collections_to_dict(self, dict: dict, item_name: str, container: any) -> list:
        """
        Adds the container, a list of items to a dictionary
        """
        if len(container) < len(dict):
            container.extend(["N/A"] * (len(dict) - len(container)))
        return list({**dict[i], item_name: container[i]} for i in range(len(dict)))

        
    def find_meaning(self, word: str, show_examples = True, show_synonyms = False, show_antonyms = False) -> list:
        """
        Find the meaning, examples, synonyms and antonyms of a word
        :param word: word to find the meaning of
        :param show_examples: whether to show examples
        :param show_synonyms: whether to show synonyms
        :param show_antonyms: whether to show antonyms
        :return: list of meanings of the word
        """
        response = requests.get(self.API_ENDPOINT + word)
        if response.status_code == 200:
            all_meanings = response.json()[0]["meanings"]
            definitions = self.__get_items("definitions", all_meanings)
            # definitions is a 2d list, make it 1d
            definitions = self.__flatten_2d_list(definitions)
            word_meaning = list(map(lambda defn: {"defn":defn["definition"]}, definitions))

            if show_examples:
                examples = self.__get_items("example", definitions)
                # unpack the dictionary word_meaning and add examples
                word_meaning = self.__add_collections_to_dict(word_meaning, "exmpls", examples)

            if show_synonyms:
                synonyms = self.__get_items("synonyms", definitions)
                # unpack the dictionary word_meaning and add synonyms 
                word_meaning = self.__add_collections_to_dict(word_meaning, "synms", synonyms)

            if show_antonyms:
                antonyms = self.__get_items("antonyms", definitions)
                # unpack the dictionary word_meaning and add antonyms 
                word_meaning = self.__add_collections_to_dict(word_meaning, "antms", antonyms)

            return word_meaning
                
        else:
            # print("Word not found")
            return None

if __name__ == "__main__":
    myDict = DictionaryAPI()
    word = "oncer"
    meanings = myDict.find_meaning(word, show_synonyms = True)
    for meaning in meanings:
        print(meaning)
    



