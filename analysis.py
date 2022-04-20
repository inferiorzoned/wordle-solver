# take all words from allFiveLetterWords.txt and create a frequency table of all possitional letters
import numpy as np
import matplotlib.pyplot as plt

allWordsSorted = open("allFiveLetterWords.txt").read().splitlines()

# create a numpy frequency array of size 5 * 26
freq = np.zeros((5, 26))

for word in allWordsSorted:
    idx = 0
    for letter in word:
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the frequency of the letter
        freq[idx][letter] += 1
        # increment the position
        idx += 1

# count frequeuncy table to weighted frequency table
freq_weights = (freq / freq.sum(axis=1, keepdims=True)) * 100
# print(freq_weights)
# print(freq)
# save the freq_weights to a file
with open("possionalLetterWeights.txt", "w") as f:
    f.write("5 positions with the probablity of each letter\n")
    for i in range(5):
        for j in range(26):
            f.write(f"{chr(ord('A') + j)} : {freq_weights[i][j]:.1f}")
            if j != 25:
                f.write(", ")
        f.write("\n")

    f.write("\n26 letters with the weighted frequency of being in 5 positions\n")
    for j in range(26):
        for i in range(5):
            f.write(f"{chr(ord('A') + j)} : {freq_weights[i][j]:.1f}")
            if i != 4:
                f.write(", ")
        f.write("\n")




# create barplots
# for n in range(5):
#     x_axis = [chr(i + ord('A')) for i in range(26)]
#     plt.bar(x_axis, freq[n])
#     plt.xlabel("Letters")
#     plt.ylabel("Percentage of Appearance")
#     plt.title(f"{n+1} Positional Letters")
#     plt.show()    

def calculate_score(word:str, freq: any) -> float:
    """
    Calculate the score of a word using the frequency table
    """
    score = 0
    for idx, letter in enumerate(word):
        # convert the letter to lowercase
        letter = letter.lower()
        # convert the letter to value of 0 - 25
        letter = ord(letter) - ord('a')
        # increment the score
        score += freq_weights[idx][letter]
    return score

# create a dict of words from allWordsSorted with their scores in one line
word_scores = map(lambda w: (w, calculate_score(w, freq)), allWordsSorted)
# sort the word scores in descending order
word_scores = sorted(word_scores, key = lambda x: x[1], reverse=True)
# print the top 50 words
for word, score in word_scores[:100]:
    print(f"{word} - {score}")

# save all word scores to a file
with open("allWordsScores.txt", "w") as f:
    for word, score in word_scores:
        f.write(f"{word} - {score}\n")
