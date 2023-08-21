from cow import CowHangman
accepted_words = ["WELLMAN HALL"]

def get_word_from_user():
    #Prompt the user to input a word or phrase for the hangman game and check against a database.
    
    def load_words_from_file(filename):
        #Load words from a file into a set.
        with open(filename, 'r') as file:
            # Read the file line by line, strip whitespace, convert to uppercase, and store in a set
            return {line.strip().upper() for line in file if line.strip()}

    def add_word_to_file(filename, word):
        #Append a word to the file.
        with open(filename, 'a') as file:
            file.write(f'\n{word}')

    filename = "Database.rtf"
    accepted_words = load_words_from_file(filename)
    
    word = input("Enter the word or phrase to be guessed (spaces are allowed): ").upper()

    # Check if the word is in the accepted words set
    if word not in accepted_words:
        choice = input(f"The word '{word}' is not in the accepted list. Would you like to add it? (yes/no): ").lower()

        if choice == "yes":
            add_word_to_file(filename, word)
            print(f"'{word}' has been added to the accepted list.")
        else:
            print("Please choose a word from the accepted list or add a new word.")
            return get_word_from_user()  # Recursive call to prompt the user again
    
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
