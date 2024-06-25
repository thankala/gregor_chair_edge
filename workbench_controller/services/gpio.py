from typing import Set, Dict

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    import Mock.GPIO as GPIO


def init_pins(pins: Set[int], board_mode: int = GPIO.BCM) -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(board_mode)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def cleanup(pin: int = None) -> None:
    if pin:
        GPIO.cleanup(pin)
    else:
        GPIO.cleanup()


def get_pin_state(pin: int) -> int | None:
    result = GPIO.input(pin)
    return result if result else 0


def set_pins_state(pin: int, state: int) -> None:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)
