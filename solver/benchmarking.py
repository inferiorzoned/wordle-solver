from wordle_solver import WordleSolver

allWordleWords = open("included.txt").read().splitlines()

wordAttemptDict = {}
attemptCount = 0
attemptSum = 0
for word in allWordleWords:
    solver = WordleSolver()
    solver.testSolver(word)
    wordAttemptDict[word] = solver.attemptsTaken
    attemptSum += solver.attemptsTaken
    attemptCount += 1
print(wordAttemptDict)
print(f"Total number of attempts are {attemptSum}")
print(f"Number of wordle words are {attemptCount}")
print(f"Average attempt is {attemptSum/attemptCount}")