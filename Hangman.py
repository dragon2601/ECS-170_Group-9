import sys
import pandas as pd
import streamlit as st
from collections import defaultdict

df = pd.read_csv("Database.csv")
word_database = df['Word'].tolist()

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

    def update_state(self, positions, letter):
        state_list = list(self.state)
        for pos in positions:
            state_list[pos] = letter
        self.state = ''.join(state_list)

class EntropyBasedPlayer:
    def __init__(self, word_database):
        self.word_database = word_database
        self.already_guessed = set()

    def filter_words(self, pattern):
        return [word for word in self.word_database if self.match_pattern(word, pattern)]

    def next_guess(self, current_state):
        possible_words = self.filter_words(current_state)

        if not possible_words:
            return None

        letter_counts = defaultdict(int)
        for word in possible_words:
            for letter in word:
                if letter not in self.already_guessed:
                    letter_counts[letter] += 1

        sorted_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)

        if sorted_letters:
            next_guess = sorted_letters[0][0]
            self.already_guessed.add(next_guess)
            return next_guess
        else:
            return None

    def match_pattern(self, word, pattern):
        if len(word) != len(pattern):
            return False

        for i in range(len(word)):
            if pattern[i] != '_' and pattern[i].lower() != word[i].lower():
                return False
        return True


    def reset_guessed(self):
        self.already_guessed = []
        self.wrong_guesses = []

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
    st.title("🎩 Hangman AI Game 🎩")
    st.write("Enter your word:")

    hangman = HangmanGame(len(target_word))
    player = EntropyBasedPlayer(word_database)
    cow_game = CowHangman()

    while "_" in hangman.get_state() and not cow_game.is_game_over() and not player.game_over:
        st.write(f"Current state: {hangman.get_state()}")
        st.write(cow_game.display())

        ai_guess = player.next_guess(hangman.get_state())
        if ai_guess:
            st.write(f"AI's guess is: {ai_guess}")

            current_pos = hangman.get_state().index("_")
            if target_word[current_pos].lower() == ai_guess:
                st.write("Right guess!")
                hangman.update_state([current_pos], ai_guess.upper())
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
    if user_word:
        play_game(user_word)
