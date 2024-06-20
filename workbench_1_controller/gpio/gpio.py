import RPi.GPIO as GPIO
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


class WorkbenchPin(Enum):
    OUT_1 = 27
    OUT_2 = 17
    OUT_3 = 22
    OUT_4 = 18

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
    # Leds
    for pin in LedPin:
        GPIO.setup(pin.value, GPIO.OUT)
    # Workbench
    for pin in WorkbenchPin:
        GPIO.setup(pin.value, GPIO.OUT)


def cleanup() -> None:
    GPIO.cleanup()


def get_pin_state(pin: LedPin | WorkbenchPin) -> State | None:
    return from_int(GPIO.input(pin.value))


def set_pin_state(pin: LedPin | WorkbenchPin, state: State) -> None:
    GPIO.output(pin.value, state.value)
