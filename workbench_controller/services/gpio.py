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


def cleanup(pin: int = None) -> None:
    GPIO.cleanup(pin)


def get_pin_state(pin: int) -> int | None:
    result = GPIO.input(pin)
    return result if result else 0


def set_pins_state(pin: Dict[int, int], board_mode: int = GPIO.BCM) -> None:
    GPIO.setmode(board_mode)
    for pin, state in pin.items():
        GPIO.output(pin, state)
