import sys
import pandas as pd
import streamlit as st
from cow import CowHangman
import random
import string



df = pd.read_csv("Database.csv")
word_database = df['Word'].tolist()
#word_database = ["WELLMAN HALL", "ARC", "ART", "APT", "APP", "ATV", "YOUNG HALL", "KEMPER HALL", "AGGIES", "GO AGS", "PAVILLION", "eureka", "mathematics", "physics"]
game_over = False

def compute_letter_weights(word_database):
    total_letters = 0
    letter_counts = {char: 0 for char in 'abcdefghijklmnopqrstuvwxyz'}
    
    for word in word_database:
        word = word.lower()  # Ensure the word is in lowercase for consistency
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
                total_letters += 1

    # Normalize to get frequencies
    letter_frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}
    
    return letter_frequencies

# Compute the weights at the start of the code
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

    def update_state(self, positions, letter):
        state_list = list(self.state)
        for pos in positions:
            state_list[pos] = letter
        self.state = ''.join(state_list)


class EntropyBasedPlayer:
    def __init__(self, word_database):
        self.word_database = word_database
        self.already_guessed = []

    def filter_words(self, word_length):
        return [word for word in self.word_database if len(word) == word_length]

    def next_guess(self, current_state):
        potential_matches = [word for word in self.filter_words(len(current_state)) if self.matches_state(word, current_state)]
    
        # If only one potential word match is left
        if len(potential_matches) == 1:
            return potential_matches[0]
    
        next_underscore_position = current_state.index("_")
    
        frequency_distribution = {}
        for word in potential_matches:
            letter = word[next_underscore_position]
            if letter not in self.already_guessed:
                frequency_distribution[letter] = frequency_distribution.get(letter, 0) + 1

        if not frequency_distribution:
            return None

        # Prioritize based on count first, and then by letter weight in case of a tie.
        guess = max(frequency_distribution, key=lambda k: (frequency_distribution[k], letter_weights.get(k, 0)))
        self.already_guessed.append(guess)
        return guess
    

    def matches_state(self, word, state):
        for w, s in zip(word, state):
            if s != '_' and w != s:
                return False
        return True

    def reset_guessed(self):
        self.already_guessed = []



class CowHangman:
    # TODO: Implement this or provide the original class
    def __init__(self):
        self.lives = 7  # Example initial value

    def lose_life(self):
        self.lives -= 1

    def is_game_over(self):
        return self.lives <= 0

    def display(self):
        # Implement a display method, or adapt from existing CowHangman code
        return f"Lives left: {self.lives}"


def play_game():
    if "hangman" not in st.session_state:
        st.session_state.hangman = HangmanGame(st.session_state.word_length)
        st.session_state.player = EntropyBasedPlayer(word_database)
        st.session_state.cow_game = CowHangman()

    if st.session_state.cow_game.is_game_over():
        st.write("Game over! AI lost.")
        if st.button("Restart"):
            del st.session_state.hangman
            del st.session_state.player
            del st.session_state.cow_game
        return

    if "_" not in st.session_state.hangman.get_state():
        st.write(f"AI successfully guessed the word {st.session_state.hangman.get_state()}!")
        if st.button("Restart"):
            del st.session_state.hangman
            del st.session_state.player
            del st.session_state.cow_game
        return

    guess = st.session_state.player.next_guess(st.session_state.hangman.get_state())
    st.write(f"AI's guess is: {guess}")

    if st.button("Correct"):
        positions = [i for i, c in enumerate(st.session_state.hangman.get_state()) if c == "_"]
        st.session_state.hangman.update_state(positions, guess)
        st.session_state.player.reset_guessed()
    elif st.button("Incorrect"):
        st.session_state.cow_game.lose_life()
        st.write(f"Lives left: {st.session_state.cow_game.lives}")
        
    st.write(f"Current state: {st.session_state.hangman.get_state()}")

if __name__ == "__main__":
    st.title("Hangman AI Game")
    st.write("Welcome to the Hangman AI game! Let the AI guess your word!")
    
    if "word_length" not in st.session_state:
        st.session_state.word_length = st.number_input("Enter the length of the word:", min_value=1, max_value=20, value=8)

    play_game()


