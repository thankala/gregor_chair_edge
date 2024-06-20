import RPi.GPIO as GPIO
from enum import Enum


class LedPin(Enum):
    FREE = 14
    ASSEMBLING = 15
    PENDING = 18

    def __str__(self):
        return self.name


class State(Enum):
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW

    def __str__(self):
        return self.value


def from_int(value: int) -> State | None:
    if value == 0:
        return State.LOW
    if value == 1:
        return State.HIGH
    return None


def init_pins() -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in LedPin:
        GPIO.setup(pin.value, GPIO.OUT)


def cleanup() -> None:
    GPIO.cleanup()


def get_pin_state(pin: LedPin) -> State | None:
    return from_int(GPIO.input(pin.value))


def set_pin_state(pin: LedPin, state: State) -> None:
    GPIO.output(pin.value, state.value)
