import typing

from workbench_controller.domain.pin import Pin
from workbench_controller.domain.state import State
from workbench_controller.domain.workbench import Workbench, FixtureState, Fixture
from workbench_controller.services.gpio import (
    set_pins_state as gpio_set_pin_state,
    get_pin_state as gpio_get_pin_state,
    cleanup as gpio_cleanup,
    init_pins as gpio_init_pins
)


def init_pins() -> None:
    try:
        gpio_init_pins({pin.value for pin in Pin})
    except Exception as e:
        raise Exception({'error': f'An error has occurred while initializing pins: {e.args}'})


def cleanup() -> None:
    try:
        gpio_cleanup()
    except Exception as e:
        raise Exception({'error': f'An error has occurred while cleaning up pins: {e.args}'})


def set_initial_state_for_fixtures(workbench: Workbench) -> None:
    try:
        for fixture in workbench.fixtures.values():
            for fixture_state, pin in workbench.get_available_states_for_given_fixture(fixture).items():
                if fixture_state == FixtureState.FREE:
                    gpio_set_pin_state({pin.value: State.HIGH.value})
                else:
                    gpio_set_pin_state({pin.value: State.LOW.value})
    except Exception as e:
        raise Exception({'error': f'An error has occurred while setting initial state for fixtures: {e.args}'})


def rotate_workbench(workbench: Workbench) -> int:
    try:
        return workbench.rotate()
    except Exception as e:
        raise Exception({'error': f'An error has occurred while rotating workbench: {e.args[0]}'})


def set_fixture_state(workbench: Workbench, fixture_name: str, state_name: str) -> typing.Dict:
    try:
        fixture = workbench.fixtures[fixture_name.upper()]
    except KeyError:
        raise Exception({'error': f'Invalid fixture: {fixture_name}'})
    try:
        state = FixtureState[state_name.upper()]
    except KeyError:
        raise Exception({'error': f'Invalid state: {state_name}'})

    try:
        states = workbench.get_available_states_for_given_fixture(fixture)
    except KeyError:
        raise Exception({'error': f'Invalid state for given fixture: {fixture_name},{state_name}'})

    if state in states:
        for fixture_state, pin in states.items():
            if fixture_state == state:
                gpio_set_pin_state({pin.value: State.HIGH.value})
            else:
                gpio_set_pin_state({pin.value: State.LOW.value})
    else:
        raise Exception({'error': f'Invalid state for given fixture: {fixture_name},{state_name}'})

    return get_fixture_state(workbench, fixture_name)


def get_fixture_state(workbench: Workbench, fixture_name: typing.Optional[str] = None) -> typing.Dict:
    result = {}
    if fixture_name:
        try:
            fixture = workbench.fixtures[fixture_name.upper()]
        except KeyError:
            raise Exception({'error': f'Invalid fixture: {fixture_name}'})

        try:
            states = workbench.get_available_states_for_given_fixture(fixture)
        except KeyError:
            raise Exception({'error': f'Invalid state for given fixture: {fixture_name}'})

        for state, pin in states.items():
            if gpio_get_pin_state(pin.value):
                result[fixture.name] = state.name

        if not result:
            raise Exception({'error': f'No state found for fixture: {fixture.name}'})
        return result

    all_fixtures = workbench.fixtures.values()
    for fixture in all_fixtures:
        states = workbench.get_available_states_for_given_fixture(fixture)
        for state, pin in states.items():
            if gpio_get_pin_state(pin.value):
                result[fixture.name] = state.name

    fixture_names = ", ".join(fixture.name for fixture in all_fixtures)
    if not result:
        raise Exception({'error': f'No state found for fixtures: {fixture_names}'})
    return result
