import RPi.GPIO as GPIO

from .state import State
from .led_pin import LedPin
from .workbench_pin import WorkbenchPin


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
