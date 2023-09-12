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

# Streamlit specific game initialization
def start_page():
    st.title("Hangman AI Game")
    st.write("Welcome to the Hangman AI game! Let the AI guess your word!")
    
    # Choose word length
    st.session_state.word_length = st.number_input("Enter the length of the word:", min_value=1, max_value=20, value=8)

    # Start game button
    if st.button("Start Game"):
        st.session_state.hangman = HangmanGame(st.session_state.word_length)
        st.session_state.player = EntropyBasedPlayer(word_database)
        st.session_state.cow_game = CowHangman()
        st.session_state.page = "game_page"


def run_game():
    st.title("Hangman AI Game")
    st.write("AI is trying to guess your word...")

    # Display current state
    st.write("Current state:", st.session_state.hangman.get_state())
    
    if "waiting_for_feedback" not in st.session_state:
        st.session_state.waiting_for_feedback = False

    # Check if AI has already guessed the word
    if "_" not in st.session_state.hangman.get_state():
        st.write("AI has successfully guessed the word!")
        st.session_state.page = "start_page"
        return

    if not st.session_state.waiting_for_feedback:
        st.session_state.guess = st.session_state.player.next_guess(st.session_state.hangman.get_state())
        st.session_state.waiting_for_feedback = True

    st.write("AI's guess:", st.session_state.guess)
    right_guess = st.button("Right Guess")
    wrong_guess = st.button("Wrong Guess")

    if right_guess or wrong_guess:
        # Process feedback
        if right_guess:
            # Update the game state with the correct guess
            positions = [i for i, char in enumerate(st.session_state.hangman.get_state()) if char == "_"]
            st.session_state.hangman.update_state(positions, st.session_state.guess)
            st.session_state.player.reset_guessed()
        
        else:  # wrong_guess
            # Update the hangman (cow) state
            st.session_state.cow_game.lose_life()
            if st.session_state.cow_game.is_game_over():
                st.write("Game Over! AI Lost!")
                st.session_state.page = "start_page"
                return

        # Allow AI to make the next guess
        st.session_state.waiting_for_feedback = False
if __name__ == "__main__":
    # Check for page in session state
    if "page" not in st.session_state:
        st.session_state.page = "start_page"

    # Page router
    if st.session_state.page == "start_page":
        start_page()
    elif st.session_state.page == "game_page":
        run_game()


    
