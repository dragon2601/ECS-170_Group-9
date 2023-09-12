import sys
import pandas as pd
import streamlit as st
from cow import CowHangman


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


def main():
    st.title('Entropy-based Hangman Game')
    
    if 'page' not in st.session_state:
        st.session_state.page = 'start'

    # Start page
    if st.session_state.page == 'start':
        if st.button('Start Game'):
            # Initialize the game's necessary variables
            st.session_state.cow_game = CowHangman()
            st.session_state.word_length = st.slider("Select the word length", 1, 100, 5)
            st.session_state.hangman = HangmanGame(st.session_state.word_length)
            st.session_state.player = EntropyBasedPlayer(word_database)
            st.session_state.page = 'game'
            
    # Game page
    elif st.session_state.page == 'game':
        st.write("Current state:", st.session_state.hangman.get_state())
        guess = st.session_state.player.next_guess(st.session_state.hangman.get_state())
        st.write(f"AI guesses: {guess}")

        if guess is None:
            st.write("AI is out of guesses!")
            if st.session_state.cow_game.lives <= 0:
                st.write("AI lost!")
                if st.button('End'):
                    st.session_state.page = 'start'
                    return

        elif len(guess) == st.session_state.word_length:
            st.write(f"Is the word {guess}?")
            if st.button('Yes'):
                st.write("AI won!")
                if st.button('End'):
                    st.session_state.page = 'start'
                    return
            elif st.button('No'):
                st.write("AI lost!")
                if st.button('End'):
                    st.session_state.page = 'start'
                    return
        else:
            st.write("Is the guess correct?")
            if st.button('Correct'):
                # Same logic as before...
                positions = [idx for idx, char in enumerate(st.session_state.hangman.get_state()) if char == "_"]
                st.session_state.hangman.update_state(positions, guess)
                st.session_state.player.reset_guessed()
            elif st.button('Incorrect'):
                st.session_state.cow_game.lose_life()
                st.write(f"Lives remaining: {st.session_state.cow_game.lives}")
                if st.session_state.cow_game.lives <= 0:
                    st.write("AI lost!")
                    if st.button('End'):
                        st.session_state.page = 'start'
                        return

if __name__ == "__main__":
    main()

    
