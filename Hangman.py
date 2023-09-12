import sys
import pandas as pd
import streamlit as st
from collections import defaultdict

df = pd.read_csv("Database.csv")
word_database = df['Word'].tolist()
word_database = [word.lower() for word in df['Word'].tolist()]


def compute_letter_weights(word_database):
    total_letters = 0
    letter_counts = {char: 0 for char in 'abcdefghijklmnopqrstuvwxyz'}
    
    for word in word_database:
        word = word.lower()  # Ensure the word is in lowercase for consistency
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
                total_letters += 1

    letter_frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}
    
    return letter_frequencies

letter_weights = compute_letter_weights(word_database)

class HangmanGame:
    def __init__(self, word_length):
        self.word_length = word_length
        self.state = "_" * word_length
        self.guesses = []

    def get_state(self):
        return self.state

    def guess(self, letter):
        self.guesses.append(letter)
        if letter in self.state:
            return True
        return False

    def update_state(self, letter):
        """Update the game state by replacing the next underscore with the given letter."""
        self.state = self.state.replace("_", letter, 1)

class EntropyBasedPlayer:
    def __init__(self, word_database):
        self.word_database = word_database
        self.already_guessed = []
        self.wrong_guesses = []  # Add this line

    def filter_words(self, current_state):
        """Filter the word database to only words that match the current state pattern."""
        word_length = len(current_state)
        return [word for word in self.word_database if len(word) == word_length and self.matches_state(word, current_state)]

    def next_guess(self, current_state):
        potential_matches = self.filter_words(current_state)
        if not potential_matches:
            return None

        next_underscore_position = current_state.index("_")
    
        # Build a frequency distribution of letters in the potential match list
        frequency_distribution = defaultdict(int)
        for word in potential_matches:
            letter = word[next_underscore_position]
            if letter not in self.already_guessed:
                frequency_distribution[letter] += 1

        # If no valid guesses are available from frequency distribution, guess a random letter
        if not frequency_distribution:
            remaining_letters = set('abcdefghijklmnopqrstuvwxyz') - set(self.already_guessed)
            if not remaining_letters:
                return None
            return random.choice(list(remaining_letters))

        # Use the frequency distribution and letter weights to determine the best guess
        guess = max(frequency_distribution, key=lambda k: (frequency_distribution[k], letter_weights.get(k, 0)))
        self.already_guessed.append(guess)
        return guess

    def matches_state(self, word, state):
        """Check if a word from the database matches the current guessed state pattern."""
        for w, s in zip(word, state):
            if s != '_' and w.lower() != s.lower():
                return False
            if s == '_' and w.lower() in self.already_guessed:
                return False
        return True

    def reset_guessed(self):
        self.already_guessed = []

class CowHangman:
    def __init__(self):
        self.lives = 7

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

    def display(self):
        return f"Lives left: {self.lives}"

def play_game(target_word):
    hangman = HangmanGame(len(target_word))
    player = EntropyBasedPlayer(word_database)
    cow_game = CowHangman()

    while "_" in hangman.get_state() and not cow_game.is_game_over():
        col1, col2 = st.columns(2)  # Create two columns

        # Display game state in the first column
        col1.write(f"Current state: {hangman.get_state()}")

        # Display cow's lives in the second column
        col2.write(cow_game.display())

        ai_guess = player.next_guess(hangman.get_state())
        if ai_guess:
            st.write(f"AI's guess is: {ai_guess}")

            current_pos = hangman.get_state().index("_")
            if ai_guess in target_word:
                st.write("Right guess!")
                hangman.update_state(ai_guess.upper())
                player.reset_guessed()
            else:
                st.write("Wrong guess!")
                player.wrong_guesses.append(ai_guess)
                cow_game.lose_life()
        else:
            st.write("AI is out of guesses.")
            break

    if "_" not in hangman.get_state():
        st.success(f"AI has successfully guessed the word: {hangman.get_state()}")
    else:
        st.error("AI couldn't guess the word!")


if __name__ == "__main__":
    st.title("🎩 Hangman AI Game 🎩")
    user_word = st.text_input("Enter your word:")
    if user_word:
        play_game(user_word.lower())


