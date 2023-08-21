from cow import CowHangman

def get_word_from_user():
    #Prompt the user to input a word or phrase for the hangman game.
    word = input("Enter the word or phrase to be guessed (spaces are allowed): ").upper()
    while not all(char.isalpha() or char.isspace() for char in word):
        print("Please only use letters and spaces.")
        word = input("Enter the word or phrase to be guessed (spaces are allowed): ").upper()
    return word


def play_hangman():
    word = get_word_from_user()
    print("\n" * 100)  # Clear the console screen to hide the input word
    guessed_letters = []
    display_word = ['_' if letter.isalpha() else letter for letter in word]
    cow_game = CowHangman()
    
    current_position = 0

    while cow_game.lives > 0 and current_position < len(word):
        print(' '.join(display_word))
        guess = input("Guess the next letter: ").upper()

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single valid letter.")
            continue

        # Check if the guess matches the current expected letter
        if guess == word[current_position]:
            # Update the display word and move to the next position
            display_word[current_position] = guess
            current_position += 1
            
            # Skip over spaces or non-alphabetic characters
            while current_position < len(word) and not word[current_position].isalpha():
                display_word[current_position] = word[current_position]
                current_position += 1
        else:
            cow_game.lose_life()
    
    if current_position == len(word):
        print("Congratulations! You've guessed the word:", word)
    else:
        print("Out of lives! The word was:", word)

play_hangman()
