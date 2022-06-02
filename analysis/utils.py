# take all the words from "included.txt"
# sort them
# save the words to "wordleWords.txt"

with open("included.txt") as f:
    included = f.read().splitlines()

included.sort()

with open("allWordleWords.txt", "w") as f:
    for word in included:
        f.write(f"{word}\n")