from enum import Enum


class BoardMode(Enum):
    BCM = 11
    BOARD = 10

    def __str__(self):
        return self.name
