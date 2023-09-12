import sys
import pandas as pd
import streamlit as st
import pandas as pd

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
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    if not st.session_state.game_started:
        st.title("Welcome to Hangman AI!")
        if st.button("Start Game"):
            st.session_state.game_started = True
            st.session_state.game_over = False
            # Initialize game states
            st.session_state.cow_game = CowHangman()
            st.session_state.word_length = st.slider("Choose the word length", min_value=1, max_value=max(map(len, word_database)), value=5)
            st.session_state.hangman = HangmanGame(st.session_state.word_length)
            st.session_state.player = EntropyBasedPlayer(word_database)
            st.session_state.correct_guess = False

    elif st.session_state.game_started and not st.session_state.game_over:
        st.title("Playing Hangman AI")
        
        st.write("Current state:", st.session_state.hangman.get_state())
        guess = st.session_state.player.next_guess(st.session_state.hangman.get_state())

        if guess is None:
            st.write("AI is out of guesses!")
            st.session_state.game_over = True
        elif len(guess) == st.session_state.word_length:
            st.write(f"AI guesses the word is: {guess}")
            st.session_state.correct_guess = st.button("Correct")
            st.session_state.wrong_guess = st.button("Incorrect")
            if st.session_state.correct_guess:
                st.write("AI won!")
                st.session_state.game_over = True
            elif st.session_state.wrong_guess:
                st.write("AI lost!")
                st.session_state.game_over = True
        else:
            st.write(f"AI guesses the letter: {guess}")
            st.session_state.correct_guess = st.button("Correct")
            st.session_state.wrong_guess = st.button("Incorrect")
            if st.session_state.correct_guess:
                # Handle the game logic for a correct guess
                positions = []
                word_list = list(st.session_state.hangman.get_state())
                for idx, char in enumerate(word_list):
                    if char == "_":
                        word_list[idx] = guess
                        positions.append(idx)
                        break
                st.session_state.hangman.update_state(positions, guess)
                st.session_state.player.reset_guessed()
            elif st.session_state.wrong_guess:
                # Handle the game logic for a wrong guess
                st.session_state.cow_game.lose_life()
                if st.session_state.cow_game.is_game_over():
                    st.write("AI lost!")
                    st.session_state.game_over = True

    if st.session_state.game_over:
        if st.button("End Game"):
            st.session_state.game_started = False


if __name__ == "__main__":
    main()
    
