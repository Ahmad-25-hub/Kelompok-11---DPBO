class Skor:
    def __init__(self, lives=3):
        self.lives = lives

    def lose_life(self):
        self.lives -= 1
