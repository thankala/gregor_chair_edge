from enum import Enum

from RPi import GPIO


class LedState(Enum):
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW

    def __str__(self):
        return self.value
