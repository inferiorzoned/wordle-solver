import requests
import csv

api_endpoint = "https://api.dictionaryapi.dev/api/v2/entries/en/"
# word = "chaos"

# Get the meanings of the word from api_endpoint
# response = requests.get(api_endpoint + word)
# print(response.json()[0]["meanings"][0]["definitions"][0]["definition"])

# sample response to request 
'''
[{"word":"chaos","phonetic":"ˈkeɪɒs","phonetics":[{"text":"ˈkeɪɒs","audio":"//ssl.gstatic.com/dictionary/static/sounds/20200429/chaos--_gb_1.mp3"}],"origin":"late 15th century (denoting a gaping void or chasm, later formless primordial matter): via French and Latin from Greek khaos ‘vast chasm, void’.","meanings":[{"partOfSpeech":"noun","definitions":[{"definition":"complete disorder and confusion.","example":"snow caused chaos in the region","synonyms":["disorder","disarray","disorganization","confusion","mayhem","bedlam","pandemonium","madness","havoc","turmoil","tumult","commotion","disruption","upheaval","furore","frenzy","uproar","hue and cry","babel","hurly-burly","a maelstrom","a muddle","a mess","a shambles","a mare's nest","anarchy","entropy","lawlessness","bangarang","hullabaloo","all hell broken loose","a madhouse","an omnishambles","a car crash","a three-ring circus"],"antonyms":["order","orderliness"]}]}]}]
'''

words_added_already = set()
# get all the words from the first column of the csv file and save in a set
with open('mydict.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row and row[0] != '':
            words_added_already.add(row[0])
        # words_added_already.add(row[0])
# print(words_added_already)

# read the words from temp_words.txt and put them in a list
def read_words(file_name):
    words = []
    with open(file_name, "r") as file:
        for line in file:
            word = line.strip()
            if word not in words_added_already:
                words.append(word)
            else:
                print("Word already added: " + word)
            # words.append(line.strip())
    return words

words = read_words("temp_words.txt")

# make a string of all the items in the list seperated by comma
def list_to_string(list):
    string = ""
    for item in list:
        string += item + ", "
    return string


not_found = set()
with open('mydict.csv', 'a', newline='') as csvfile:
    # fieldnames = ['Word', 'Definition', 'Example', 'Synonyms', 'Antonyms']
    writer = csv.writer(csvfile)
    for word in words:
        response = requests.get(api_endpoint + word)
        for i in range(len(response.json())):
            # word = response.json()[i]["word"]
            # check if response.json() is dict and title no definitions found
            if isinstance(response.json(), dict) and response.json()["title"] == "No Definitions Found":
                print("No definitions found for word: " + word)
                not_found.add(word)
                continue
            for j in range(len(response.json()[i]["meanings"])):
                # print(j)
                for k in range(len(response.json()[i]["meanings"][j]["definitions"])):
                    definition = response.json()[i]["meanings"][j]["definitions"][k]["definition"]
                    example = response.json()[i]["meanings"][j]["definitions"][k]["example"]
                    synonyms = response.json()[i]["meanings"][j]["definitions"][k]["synonyms"]
                    antonyms = response.json()[i]["meanings"][j]["definitions"][k]["antonyms"]
                    # write the definition, example, synonym and antonyms in the second column in four rows
                    writer.writerow((word, "def: " + definition))
                    if example: 
                        writer.writerow(('',"exmpl: " + example))
                    if synonyms: 
                        writer.writerow(('',"syno: " + list_to_string(synonyms)))
                    if antonyms: 
                        writer.writerow(('',"anto: " + list_to_string(antonyms)))

# write the words to not_found.txt that are not found in the dictionary
with open("not_found.txt", "a") as file:
    for word in not_found:
        file.write(word + "\n")