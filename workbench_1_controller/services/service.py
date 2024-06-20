import time

from workbench_1_controller.gpio.gpio import (
    cleanup,
    init_pins,
    get_pin_state,
    set_pin_state,
    WorkbenchPin,
    LedPin,
    State
)


def gpio_init_pins() -> None:
    init_pins()


def gpio_cleanup() -> None:
    cleanup()


def gpio_get_pin_state(pin: LedPin | WorkbenchPin) -> State | None:
    return get_pin_state(pin)


def gpio_set_pin_state(pin: LedPin | WorkbenchPin, state: State) -> None:
    return set_pin_state(pin, state)


def workbench_rotate() -> None:
    Direction = 2
    Step = 0
    for ItemNo in range(1):
        for Step in range(130, 0, -1):
            if Direction == 0:
                set_pin_state(WorkbenchPin.OUT_1, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, State.LOW)
                set_pin_state(WorkbenchPin.OUT_3, State.LOW)
                set_pin_state(WorkbenchPin.OUT_4, State.LOW)
                time.sleep(0.008)
            elif Direction == 1:
                set_pin_state(WorkbenchPin.OUT_1, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, State.LOW)
                set_pin_state(WorkbenchPin.OUT_4, State.LOW)
                time.sleep(0.008)
            elif Direction == 2:
                set_pin_state(WorkbenchPin.OUT_1, State.LOW)
                set_pin_state(WorkbenchPin.OUT_2, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, State.LOW)
                set_pin_state(WorkbenchPin.OUT_4, State.LOW)
                time.sleep(0.008)
            elif Direction == 3:
                set_pin_state(WorkbenchPin.OUT_1, State.LOW)
                set_pin_state(WorkbenchPin.OUT_2, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, State.LOW)
                time.sleep(0.008)
            elif Direction == 4:
                set_pin_state(WorkbenchPin.OUT_1, State.LOW)
                set_pin_state(WorkbenchPin.OUT_2, State.LOW)
                set_pin_state(WorkbenchPin.OUT_3, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, State.LOW)
                time.sleep(0.008)
            elif Direction == 5:
                set_pin_state(WorkbenchPin.OUT_1, State.LOW)
                set_pin_state(WorkbenchPin.OUT_2, State.LOW)
                set_pin_state(WorkbenchPin.OUT_3, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, State.HIGH)
                time.sleep(0.008)
            elif Direction == 6:
                set_pin_state(WorkbenchPin.OUT_1, State.LOW)
                set_pin_state(WorkbenchPin.OUT_2, State.LOW)
                set_pin_state(WorkbenchPin.OUT_3, State.LOW)
                set_pin_state(WorkbenchPin.OUT_4, State.HIGH)
                time.sleep(0.008)
            elif Direction == 7:
                set_pin_state(WorkbenchPin.OUT_1, State.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, State.LOW)
                set_pin_state(WorkbenchPin.OUT_3, State.LOW)
                set_pin_state(WorkbenchPin.OUT_4, State.HIGH)
                time.sleep(0.008)
            if Direction == 0:
                Direction = 7
                continue
            Direction = Direction - 1
