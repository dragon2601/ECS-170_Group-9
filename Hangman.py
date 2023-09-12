import sys
import pandas as pd
import streamlit as st
from cow import CowHangman
import random
from collections import defaultdict

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
        self.wrong_guesses = []  # Added this line to keep track of wrong guesses

    def filter_words(self, word_length):
        return [word for word in self.word_database if len(word) == word_length]

    '''def next_guess(self, current_state):
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
        return guess'''
    def next_guess(self, current_state):
        next_position_to_guess = current_state.index('_')

        # Filter words in the database based on the current state
        possible_words = [word for word in self.word_database if self.match_pattern(word, current_state)]

        # If there are no possible words left, return None
        if not possible_words:
            return None

        letter_counts = defaultdict(int)

        # Count the occurrence of each letter in the next position among the possible words
        for word in possible_words:
            letter = word[next_position_to_guess].lower()
            if letter not in self.wrong_guesses:  # Ensure that the letter hasn't been guessed incorrectly
                letter_counts[letter] += 1

        # Sort the letters by their counts and get the most frequent one
        sorted_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)

        if sorted_letters:
            return sorted_letters[0][0].lower()
        else:
            return None
        
        return guessed_letter
    

    def match_pattern(self, word, pattern):
        # Only consider words of the same length
        if len(word) != len(pattern):
            return False

        # Check if word matches the given pattern
        for i in range(len(word)):
            if pattern[i] != '_' and pattern[i].lower() != word[i].lower():
                return False

        return True


    def matches_state(self, word, state):
        for w, s in zip(word, state):
            if s != '_' and w != s:
                return False
        return True

    def reset_guessed(self):
        self.already_guessed = []
        self.wrong_guesses = []  # Clear wrong guesses when a right guess is made



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


def play_game(target_word):
    st.title("Hangman AI Game")
    st.write("Welcome to the Hangman AI game! Let's see if the AI can guess your word.")

    # Initialize the game and player
    hangman = HangmanGame(len(target_word))
    player = EntropyBasedPlayer(word_database)
    cow_game = CowHangman()

    while "_" in hangman.get_state() and not cow_game.is_game_over():
        st.write(f"Current state: {hangman.get_state()}")

        # Display the AI's guess
        ai_guess = player.next_guess(hangman.get_state())
        if ai_guess:
            st.write(f"AI's guess is: {ai_guess}")
        else:
            st.write("AI is out of guesses.")

        # Check if the guess is in the current position to be revealed
        current_pos = hangman.get_state().index("_")  # Get the first underscore position

        if target_word[current_pos].lower() == ai_guess:  # Ensure a case insensitive comparison
            st.write("Right guess!")
            hangman.update_state([current_pos], ai_guess.upper())  # Update state with the correct letter's case
            player.reset_guessed()
        else:
            st.write("Wrong guess!")
            player.wrong_guesses.append(ai_guess)
            cow_game.lose_life()

    if "_" not in hangman.get_state():
        st.success(f"AI has successfully guessed the word: {hangman.get_state()}")
    else:
        st.error("AI couldn't guess the word!")


if __name__ == "__main__":
    user_word = st.text_input("Enter your word:").upper()  # Assuming words in database are uppercase
    if user_word:
        play_game(user_word)






