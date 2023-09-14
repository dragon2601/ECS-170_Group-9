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
        word = word.lower()
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
        self.state = self.state.replace("_", letter, 1)

class EntropyBasedPlayer:
    def __init__(self, word_database):
        self.word_database = word_database
        self.already_guessed = []
        self.wrong_guesses = []

    def filter_words(self, current_state):
        word_length = len(current_state)
        potential_matches = [word for word in self.word_database if len(word) == word_length]
        #for i in potential_matches:
            #st.write(i)
        filtered_words = [word for word in potential_matches if self.matches_state(word, current_state)]
        #for i in filtered_words:
            #st.write(i)
        return filtered_words

    def next_guess(self, current_state):
        potential_matches = self.filter_words(current_state)
        if not potential_matches:
            return None

        position_to_guess = current_state.index("_")
        frequency_distribution = defaultdict(int)
        for word in potential_matches:
            letter = word[position_to_guess]
            if letter not in self.already_guessed:
                frequency_distribution[letter] += 1

        if not frequency_distribution:
            return None

        guess = max(frequency_distribution, key=lambda k: (frequency_distribution[k], letter_weights.get(k, 0)))
        self.already_guessed.append(guess)
        return guess

    def matches_state(self, word, state):
    
        for w, s in zip(word, state):
            if s != '_' and w.lower() != s.lower():
                return False
    
        position = state.index('_')

        if word[position] in self.wrong_guesses:
            return False
        
        return True

    def reset_guessed(self):
        self.already_guessed = []
        self.wrong_guesses = []

class CowHangman:
    def __init__(self):
        self.lives = 6
        self.cow_parts = [
            '''
        ^__^

        (oo)


        ''',
            '''
        ^__^

        (oo)\\_______


        ''',
            '''
        ^__^

        (oo)\\_______

        (__)\\       


        ''',
            '''
        ^__^

        (oo)\\_______

        (__)\\       )\\/\\


        ''',
            '''
        ^__^

        (oo)\\_______

        (__)\\       )\\/\\

            ||----w |
            

        ''',
            '''
        ^__^

        (oo)\\_______

        (__)\\       )\\/\\

            ||----w |
            ||     ||

        '''
        ]



    def display_cow(self):
        parts_to_display = min(5, 6 - self.lives)
        for line in self.cow_parts[parts_to_display].split('\n'):
            st.write(line)


    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.display_cow()
        else:
            st.write("No more lives!")

    def is_game_over(self):
        return self.lives <= 0

    def display(self):
        return f"Lives left: {self.lives}"

def play_game(target_word):
    hangman = HangmanGame(len(target_word))
    player = EntropyBasedPlayer(word_database)
    cow_game = CowHangman()

    while "_" in hangman.get_state() and not cow_game.is_game_over():
        col1, col2 = st.columns(2)

        col1.write(f"Current state: {hangman.get_state()}")
        col2.write(cow_game.display())

        ai_guess = player.next_guess(hangman.get_state())
        if ai_guess:
            st.write(f"AI's guess is: {ai_guess}")

            current_pos = hangman.get_state().index("_")
            if target_word[current_pos].lower() == ai_guess:
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
        st.write("Congratulations! The AI successfully guessed the word!")
    elif cow_game.is_game_over():
        st.write("Game Over. The AI couldn't guess the word.")

def information_section():
    st.sidebar.header('📖 Information Section 📖')
    
    st.sidebar.write('**1. Brief Overview of the Project**')
    st.sidebar.write('This project is a Hangman game where the AI tries to guess the word provided by the user.')

    st.sidebar.write('**2. Key AI methodologies and techniques employed**')
    st.sidebar.write('The AI uses frequency analysis and word filtering based on user feedback to narrow down possible word choices. It leverages entropy for making educated guesses.')

    st.sidebar.write('**3. Challenges faced and their resolutions**')
    st.sidebar.write('One of the main challenges was handling repeated letters in words and efficiently filtering the database of words based on the game’s current state. This was resolved by refining the word filtering algorithm and leveraging a weighted letter-frequency methodology.')
    
    st.sidebar.write('**Team Members and Contributions:**')
    
    st.sidebar.write('**Olive Manupau:**')
    st.sidebar.markdown('- Project Support Specialist')
    st.sidebar.markdown('- Assisted in creating the database')
    st.sidebar.markdown('- Took active part in brainstorming') 
    st.sidebar.markdown('- Wrote down and assisted in peer reviews') 
    st.sidebar.markdown('- Assisted in the making of the Project Presentation')

    st.sidebar.write('**Julie Khalilieh Romman:**')
    st.sidebar.markdown('- Project Manager')
    st.sidebar.markdown('- Coordinated team tasks and maintained the project timeline')
    st.sidebar.markdown('- Researched algorithms')
    st.sidebar.markdown('- Debugged code and contributed in adding words to the database.')
    st.sidebar.markdown('- Made the Project Presentation')
    

    st.sidebar.write('**Muhammad Reza:**')
    st.sidebar.markdown('- Database Manager')
    st.sidebar.markdown('- Helped compile the database for AI hangman and wrote code to allow user to append thier word to the database')

    st.sidebar.write('**Alex Prado:**')
    st.sidebar.markdown('- Preliminary Contributor')
    st.sidebar.markdown('- Gave initial patterns we could use for AI')
    st.sidebar.markdown('- Thought about multiple AI\'s we could use')

    st.sidebar.write('**Atharav Ganesh Samant:**')
    st.sidebar.markdown('- Lead Developer')
    st.sidebar.markdown('- Developed the Game')
    st.sidebar.markdown('- Wrote code that used the AI in the game')
    st.sidebar.markdown('- Created the AI logic needed and implemented that in the game')
    st.sidebar.markdown('- Developed the Website')


if __name__ == "__main__":
    st.title("🐄 Hangman AI Game 🐄")
    information_section()
    st.header("ECS 170 - GROUP 9")
    user_word = st.text_input("Enter your word:")
    if user_word:
        play_game(user_word.lower())
