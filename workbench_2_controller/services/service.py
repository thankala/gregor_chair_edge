import time

from workbench_2_controller.gpio.gpio import (
    cleanup,
    init_pins,
    get_pin_state,
    set_pin_state,
    LedPin,
    State
)


def gpio_init_pins() -> None:
    init_pins()


def gpio_cleanup() -> None:
    cleanup()


def gpio_get_pin_state(pin: LedPin) -> State | None:
    return get_pin_state(pin)


def gpio_set_pin_state(pin: LedPin, state: State) -> None:
    return set_pin_state(pin, state)
