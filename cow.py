class CowHangman:
    def __init__(self):
        self.lives = 6

        # Define the cow's parts
        self.cow_parts = [
            '''
             ^__^
            ''',
            '''
             (oo)
            ''',
            '''\_______
            ''',
            '''
             (__)\       
            ''',
            '''   )\/\\
            ''',
            '''
                 ||----w |
                 ||     ||
            '''
        ]

    def display_cow(self):
        parts_to_display = 6 - self.lives
        print("\n".join(self.cow_parts[:parts_to_display]))

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.display_cow()
        else:
            print("No more lives!")

# Example usage:

#cow_game = CowHangman()
#cow_game.lose_life()
   
