import random

class Dice:
    def __init__(self, face: int) -> None:
        self.face = face
        
    def roll(self) -> int:
        return random.randint(1, self.face)