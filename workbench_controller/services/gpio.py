import threading
from typing import Set, Dict

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    import Mock.GPIO as GPIO

_lock = threading.Lock()


def init_pins(pins: Set[int], board_mode: int = None) -> None:
    with _lock:
        GPIO.setwarnings(False)
        if board_mode:
            GPIO.setmode(board_mode)
        else:
            GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)


def cleanup(pin: int = None) -> None:
    with _lock:
        if pin:
            GPIO.cleanup(pin)
        else:
            GPIO.cleanup()


def get_pin_state(pin: int) -> int | None:
    result = GPIO.input(pin)
    return result if result else 0


def set_pins_state(pin: Dict[int, int], board_mode: int = None) -> None:
    with _lock:
        # if board_mode:
        #     GPIO.setmode(board_mode)
        # else:
        #     GPIO.setmode(GPIO.BCM)
        for pin, state in pin.items():
            GPIO.output(pin, state)
