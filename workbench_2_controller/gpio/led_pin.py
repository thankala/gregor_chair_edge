from enum import Enum


class LedPin(Enum):
    FREE = 14
    ASSEMBLING = 15
    PENDING = 18

    def __str__(self):
        return self.name
