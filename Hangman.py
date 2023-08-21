from cow import CowHangman

def play_hangman():
    word = "Wellman Hall".upper()
    guessed_letters = []
    display_word = ['_' if letter.isalpha() else letter for letter in word]
    cow_game = CowHangman()
    
    while cow_game.lives > 0 and '_' in display_word:
        print(' '.join(display_word))
        guess = input("Guess a letter: ").upper()

        if guess in guessed_letters:
            print("You've already guessed that letter!")
            continue
        
        if guess in word:
            for index, letter in enumerate(word):
                if letter == guess:
                    display_word[index] = guess
        else:
            cow_game.lose_life()

        guessed_letters.append(guess)
    
    if '_' not in display_word:
        print("Congratulations! You've guessed the word:", word)
    else:
        print("Out of lives! The word was:", word)

play_hangman()
