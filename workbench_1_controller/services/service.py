import time
import typing

from workbench_1_controller.gpio.gpio import cleanup, init_pins, get_pin_state, set_pin_state
from workbench_1_controller.gpio.led_pin import LedPin
from workbench_1_controller.gpio.led_state import LedState
from workbench_1_controller.gpio.workbench_pin import WorkbenchPin
from workbench_1_controller.services.fixtures import Fixture, FixtureState, get_available_states_for_given_fixture


def gpio_init_pins() -> None:
    init_pins()


def gpio_cleanup() -> None:
    cleanup()


def gpio_get_pin_state() -> typing.Dict:
    try:
        result = {pin.name: get_pin_state(pin).name for pin in LedPin}
    except KeyError as k:
        raise Exception({'error': f'An error has occurred while accessing pin states : {k.args}'})
    return result


def gpio_set_pin_state(data: typing.Dict) -> typing.Dict:
    for pin_name, state_name in data.items():
        try:
            pin = LedPin[pin_name.upper()]
        except KeyError:
            raise Exception({'error': f'Invalid pin: {pin_name}'})

        try:
            state = LedState[state_name.upper()]
        except KeyError:
            raise Exception({'error': f'Invalid state: {state_name}'})

        set_pin_state(pin, state)

    states = {pin.name: get_pin_state(pin).name for pin in LedPin}
    return states


def set_fixture_state(data: typing.Dict) -> typing.Dict:
    fixture_name = data.get('fixture')
    state_name = data.get('state')
    try:
        fixture = Fixture[fixture_name.upper()]
    except KeyError:
        raise Exception({'error': f'Invalid fixture: {fixture_name}'})

    try:
        state = FixtureState[state_name.upper()]
    except KeyError:
        raise Exception({'error': f'Invalid state: {state_name}'})

    try:
        states = get_available_states_for_given_fixture(fixture)
    except KeyError:
        raise Exception({'error': f'Invalid state for given fixture: {fixture_name},{state_name}'})

    if state in states:
        if state == FixtureState.FREE:
            set_pin_state(LedPin.FREE, LedState.HIGH)
            set_pin_state(LedPin.ASSEMBLING, LedState.LOW)
            set_pin_state(LedPin.PENDING, LedState.LOW)
        elif state == FixtureState.ASSEMBLING:
            set_pin_state(LedPin.FREE, LedState.LOW)
            set_pin_state(LedPin.ASSEMBLING, LedState.HIGH)
            set_pin_state(LedPin.PENDING, LedState.LOW)
        elif state == FixtureState.PENDING:
            set_pin_state(LedPin.FREE, LedState.LOW)
            set_pin_state(LedPin.ASSEMBLING, LedState.LOW)
            set_pin_state(LedPin.PENDING, LedState.HIGH)


def workbench_rotate() -> None:
    Direction = 2
    for ItemNo in range(1):
        for Step in range(130, 0, -1):
            if Direction == 0:
                set_pin_state(WorkbenchPin.OUT_1, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_3, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_4, LedState.LOW)
            elif Direction == 1:
                set_pin_state(WorkbenchPin.OUT_1, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_4, LedState.LOW)
            elif Direction == 2:
                set_pin_state(WorkbenchPin.OUT_1, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_2, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_4, LedState.LOW)
            elif Direction == 3:
                set_pin_state(WorkbenchPin.OUT_1, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_2, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_3, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, LedState.LOW)
            elif Direction == 4:
                set_pin_state(WorkbenchPin.OUT_1, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_2, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_3, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, LedState.LOW)
            elif Direction == 5:
                set_pin_state(WorkbenchPin.OUT_1, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_2, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_3, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_4, LedState.HIGH)
            elif Direction == 6:
                set_pin_state(WorkbenchPin.OUT_1, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_2, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_3, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_4, LedState.HIGH)
            elif Direction == 7:
                set_pin_state(WorkbenchPin.OUT_1, LedState.HIGH)
                set_pin_state(WorkbenchPin.OUT_2, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_3, LedState.LOW)
                set_pin_state(WorkbenchPin.OUT_4, LedState.HIGH)
            if Direction == 0:
                Direction = 7
                continue
            time.sleep(0.008)
            Direction = Direction - 1
