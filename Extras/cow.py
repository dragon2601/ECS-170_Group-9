# cow.py
class CowHangman:
    def __init__(self):
        self.lives = 6

        # Define the cow's parts in an accumulative manner
        self.cow_parts = [
            '''
             ^__^
            ''',
            '''
             ^__^
             (oo)
            ''',
            '''
             ^__^
             (oo)\_______
            ''',
            '''
             ^__^
             (oo)\_______
             (__)\       
            ''',
            '''
             ^__^
             (oo)\_______
             (__)\       )\/\\
            ''',
            '''
             ^__^
             (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
            '''
        ]
        
    def display_cow(self):
        parts_to_display = min(5, 6 - self.lives)  # This ensures that the maximum value of parts_to_display is 5
        print(self.cow_parts[parts_to_display])


    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.display_cow()
        else:
            print("No more lives!")
