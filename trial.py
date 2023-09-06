word_database = ["WELLMAN HALL", "ARC", "ART", "APT", "APP", "ATV", "YOUNG HALL", "KEMPER HALL", "AGGIES", "GO AGS", "PAVILLION", "eureka", "mathematics", "physics"]

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
        next_underscore_position = current_state.index("_")
        
        frequency_distribution = {}
        for word in potential_matches:
            letter = word[next_underscore_position]
            if letter not in self.already_guessed:
                frequency_distribution[letter] = frequency_distribution.get(letter, 0) + 1

        if not frequency_distribution:
            return None

        guess = max(frequency_distribution, key=frequency_distribution.get)
        self.already_guessed.append(guess)
        return guess

    def matches_state(self, word, state):
        for w, s in zip(word, state):
            if s != '_' and w != s:
                return False
        return True

    def reset_guessed(self):
        self.already_guessed = []

if __name__ == "__main__":
    word_length = int(input("Enter the length of the word: "))
    hangman = HangmanGame(word_length)
    player = EntropyBasedPlayer(word_database)

    while "_" in hangman.get_state():
        print("Current state:", hangman.get_state())
        guess = player.next_guess(hangman.get_state())
        if guess is None:
            print("AI is out of guesses!")
            break
        print("AI guesses:", guess)
        is_correct = input("Is the guess correct? (y/n): ").lower()
        if is_correct == 'y':
            positions = []
            word_list = list(hangman.get_state())
            for idx, char in enumerate(word_list):
                if char == "_":
                    word_list[idx] = guess
                    positions.append(idx)
                    break
            hangman.update_state(positions, guess)
            player.reset_guessed()
        else:
            print("Guess is incorrect.")

    if "_" not in hangman.get_state():
        print("AI won!")
    else:
        print("AI lost!")
