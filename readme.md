This is the benchmarking after overfitting the test set. i.e. discarding other existing five letter words, and taking only the wordle words. 

The average attempt is now 3.81 and the accuracy is almost 99.395%.

# How to Run

Go to solver directory

Run the wordle_solver.py file

Run testSolver(word) to run (simulate) against a given word

Run runSolver() to run against a hidden word (actual wordle game)

Change debugMode from config.py to 0 (no info print), or 1 (additional info print)

Toggle dictionaryMode to True in the solver to see the dictionary meaning of the words (if the word exists in the dictionaryAPI)
