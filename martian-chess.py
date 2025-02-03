import pygame # type: ignore
import images

class Die():
    
    def __init__(self):
        self.moves = []

    def click(self) -> None:
        self.display_moves()

    def display_moves(self) -> None:
        pass
    
    def place(self, column: int, row: int) -> None:
        pass
    
    def capture(self) -> None:
        pass

class Pawn(Die):
    def __init__(self):
        super().__init__()

class Drone(Die):
    def __init__(self):
        super().__init__()

class Queen(Die):
    def __init__(self):
        super().__init__()