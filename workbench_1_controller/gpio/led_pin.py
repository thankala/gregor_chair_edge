from enum import Enum


class LedPin(Enum):
    P1_FREE = 13
    P1_ASSEMBLING = 19
    P1_COMPLETED = 26

    P2_FREE = 12
    P2_ASSEMBLING = 16
    P2_PENDING = 20
    P2_COMPLETED = 21

    P3_FREE = 15
    P3_ASSEMBLING = 5
    P3_COMPLETED = 6

    def __str__(self):
        return self.name
