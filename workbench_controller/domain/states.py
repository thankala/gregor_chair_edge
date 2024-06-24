from enum import Enum


class States(Enum):
    LOW = 0
    HIGH = 1

    def __str__(self):
        return self.value
