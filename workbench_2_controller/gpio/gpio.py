import RPi.GPIO as GPIO

from workbench_2_controller.gpio.led_state import LedState
from workbench_2_controller.gpio.led_pin import LedPin


def from_int(value: int) -> LedState | None:
    if value == 0:
        return LedState.LOW
    if value == 1:
        return LedState.HIGH
    return None


def init_pins() -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in LedPin:
        GPIO.setup(pin.value, GPIO.OUT)


def cleanup() -> None:
    GPIO.cleanup()


def get_pin_state(pin: LedPin) -> LedState | None:
    return from_int(GPIO.input(pin.value))


def set_pin_state(pin: LedPin, state: LedState) -> None:
    GPIO.output(pin.value, state.value)
