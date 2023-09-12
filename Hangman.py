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
    def filter_words(self, current_state):
        """Filter the word database to only words that match the current state pattern."""
        word_length = len(current_state)
        filtered_words = [word for word in self.word_database if len(word) == word_length and self.matches_state(word, current_state)]
    
        # Add a debugging line to check if "Voorhies" is in the filtered list.
        if "voorhies" in filtered_words:
            st.write("Voorhies is a potential match!")
        else:
            st.write("Voorhies is NOT a potential match!")
    
        return filtered_words


    def next_guess(self, current_state):
        potential_matches = self.filter_words(current_state)
        if not potential_matches:
            return None

        # Build a frequency distribution of letters in the potential match list for the first underscore
        frequency_distribution = defaultdict(int)
        for word in potential_matches:
            letter = word[current_state.index("_")]  # Considering the letter at the current underscore
            if letter not in self.already_guessed:
                frequency_distribution[letter] += 1

        # If no new letters are available, return None (AI runs out of guesses)
        if not frequency_distribution:
            return None

        # Use the frequency distribution to determine the best guess (without considering the letter_weights for now)
        guess = max(frequency_distribution, key=frequency_distribution.get)
        self.already_guessed.append(guess)
        return guess


    def matches_state(self, word, state):
        """Check if a word from the database matches the current guessed state pattern."""
        for w, s in zip(word, state):
            if s != '_' and w.lower() != s.lower():
                return False
        position = state.index('_')  # Get the current guessing position
        if word[position] in self.wrong_guesses:  # Check only the current position against wrong guesses
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
            if target_word[current_pos].lower() == ai_guess:
                st.write("Right guess!")
                hangman.update_state(ai_guess.upper())
                player.reset_guessed()  # Resetting the guessed letters for the next position
            else:
                st.write("Wrong guess!")
                cow_game.lose_life()
        else:
            st.write("AI is out of guesses.")
            break

if __name__ == "__main__":
    st.title("🎩 Hangman AI Game 🎩")
    user_word = st.text_input("Enter your word:")
    if user_word:
        play_game(user_word.lower())
