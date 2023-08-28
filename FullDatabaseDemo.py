import math
from collections import Counter
import pandas as pd

df = pd.read_csv("Database.csv")

# Hangman Class
class Hangman:
    def __init__(self):
        self.guesses = set()
        self.state = []

    def update_state(self, letter: str, positions: list):
        for pos in positions:
            self.state[pos] = letter
        self.guesses.add(letter)

    def get_state(self) -> str:
        return ''.join(self.state)

# Entropy-Based AI Player
class EntropyBasedPlayer:
    def __init__(self, word_database):
        self.word_database = word_database
        
    # Conditional entropy is used to calculate probablistic likelyhood of getting a letter correct: 
    # The entropy H(X) serves as a measure of the uncertainty or randomness associated with the outcomes of the random variable X. 
    # The entropy \( H(X) \) of a discrete random variable \( X \) is defined as:
    # \[
    # H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)
    # \]
    # where \( \mathcal{X} \) is the set of all possible values that \( X \) can take, and \( p(x) \) is 
    # the probability mass function of \( X \).
    def calculate_entropy(self, frequency_distribution):
        total = sum(frequency_distribution.values())
        entropy = -sum((count / total) * math.log2(count / total) for count in frequency_distribution.values())
        return entropy

    
    # We are going to set filtered_words to the entire database to finally eliminate the words that do not match the criterium:
    # Lenght of words
    # Letters and their corresponding positions
    # If only one word fits the criteria, guess the entired word
    # Guess the most likely letter (the one with tthe lowest entropy) 
    def next_guess(self, current_state, previous_guesses):
        filtered_words = self.word_database

        # Filtering by length first
        if len(current_state) > 0:
            filtered_words = [word for word in filtered_words if len(word) == len(current_state)]
        
        # Further filtering based on known letters
        for i, char in enumerate(current_state):
            if char != "_":
                filtered_words = [word for word in filtered_words if word[i] == char]
                
        # If only one word is left, guess the entire word
        if len(filtered_words) == 1:
            return filtered_words[0]

        # Calculating letter frequencies and entropies:
        # "".join(filtered_words): This part concatenates all the words in filtered_words into a single long string.
        # Counter(...): This uses Python's collections.Counter to count the occurrences of each letter in that long string. 
        # The result is stored in a dictionary-like object frequency_distribution where the keys are the unique letters and 
        # the values are the frequencies of these letters.
        # For example, if filtered_words = ["apple", "banana"], then the frequency_distribution would 
        # look like {'a': 4, 'p': 2, 'l': 1, 'e': 1, 'b': 1, 'n': 2}.
        frequency_distribution = Counter("".join(filtered_words))
        
        # This loop iterates through each character in current_state, which is the current revealed state of 
        # the word (e.g., "_ppl_" for "apple").
        # If a character (that is not an underscore _) appears in frequency_distribution, it is eliminated. 
        # This ensures that the AI does not guess a letter it has already guessed or that has already been revealed.
        for guessed in current_state:
            if guessed in frequency_distribution:
                del frequency_distribution[guessed]
        
        # This will prevent the AI from guessing the same letter repeatedly
        for guessed in previous_guesses:
            if guessed in frequency_distribution:
                del frequency_distribution[guessed]
                
        # This checks if frequency_distribution is empty. If it is, the function returns None, which would happen 
        # if all possible letters have already been guessed or revealed, leaving the AI with no more options for guessing
        if not frequency_distribution:
            return None

        # Guessing the letter with the lowest entropy (the most likely letter based on entropy criteria)
        # Notice that self.calculate_entropy computes entropy
        min_entropy_letter = min(frequency_distribution, key=lambda x: self.calculate_entropy({x: frequency_distribution[x]})) 
        return min_entropy_letter

# A sample word database which replace with actual database later)
word_database = df.iloc[:,0]

# Initializing game and AI player
hangman = Hangman()
player = EntropyBasedPlayer(word_database)
ask = False
# Game 
while True:
    if hangman.get_state():
        print(f"Current state: {hangman.get_state()}")

    next_guess = player.next_guess(hangman.get_state(), hangman.guesses)

    if next_guess and len(next_guess) > 1:
        print(f"AI guesses the entire word: {next_guess}")
        is_correct = input("Is the AI correct? (y/n): ").strip().lower() == 'y'
        if is_correct:
            print("AI won!")
            break
        else:
            print("AI was wrong.")
            break

    if next_guess is None:
        print("AI gives up.")
        break
    if ask == False:
        word_length = int(input("Enter the length of the word: "))
        hangman.state = ["_"] * word_length
        ask = True
    print(f"AI guesses: {next_guess}")

    is_correct = input(f"Is the guess correct? (y/n): ").strip().lower() == 'y'
    
    if is_correct:
        positions = list(map(int, input("Enter the positions (0-based) of the letter, separated by spaces: ").split()))
        hangman.update_state(next_guess, positions)
    else:
        hangman.guesses.add(next_guess)
        print("Guess is incorrect.")
    '''if is_correct:
        if not hangman.state:
            word_length = int(input("Enter the length of the word: "))
            hangman.state = ["_"] * word_length
        positions = list(map(int, input("Enter the positions (0-based) of the letter, separated by spaces: ").split()))
        hangman.update_state(next_guess, positions)
    else:
        hangman.guesses.add(next_guess)
        print("Guess is incorrect.")'''

    if hangman.state and "_" not in hangman.get_state():
        print("AI won!")
        break
