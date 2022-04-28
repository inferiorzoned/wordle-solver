# take all the words from "included.txt"
# take all the words from "not_included.txt"

# merge all the words and sort them
# save the words to "allWords.txt"

with open("included.txt") as f:
    included = f.read().splitlines()

with open("not_included.txt") as f:
    not_included = f.read().splitlines()

allWords = included + not_included
allWords.sort()

with open("allWords.txt", "w") as f:
    for word in allWords:
        f.write(f"{word}\n")