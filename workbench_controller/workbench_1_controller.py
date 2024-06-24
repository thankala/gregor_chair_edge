import time

from domain.board_mode import BoardMode
from domain.state import State
from services.gpio import set_pins_state
from controllers.controller import create_app
from services.service import cleanup, init_pins, set_initial_state_for_fixtures
from domain.pin import Pin
from domain.workbench import Workbench, Fixture, FixtureState

out1 = Pin.P13.value
out2 = Pin.P11.value
out3 = Pin.P15.value
out4 = Pin.P12.value


def workbench_rotate() -> None:
    direction = 2
    for item in range(1):
        for step in range(130, 0, -1):
            if direction == 0:
                set_pins_state({
                    out1: State.HIGH.value,
                    out2: State.LOW.value,
                    out3: State.LOW.value,
                    out4: State.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 1:
                set_pins_state({
                    out1: State.HIGH.value,
                    out2: State.HIGH.value,
                    out3: State.LOW.value,
                    out4: State.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 2:
                set_pins_state({
                    out1: State.LOW.value,
                    out2: State.HIGH.value,
                    out3: State.LOW.value,
                    out4: State.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 3:
                set_pins_state({
                    out1: State.LOW.value,
                    out2: State.HIGH.value,
                    out3: State.HIGH.value,
                    out4: State.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 4:
                set_pins_state({
                    out1: State.LOW.value,
                    out2: State.LOW.value,
                    out3: State.HIGH.value,
                    out4: State.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 5:
                set_pins_state({
                    out1: State.LOW.value,
                    out2: State.LOW.value,
                    out3: State.HIGH.value,
                    out4: State.HIGH.value
                }, BoardMode.BOARD.value)
            elif direction == 6:
                set_pins_state({
                    out1: State.LOW.value,
                    out2: State.LOW.value,
                    out3: State.LOW.value,
                    out4: State.HIGH.value
                }, BoardMode.BOARD.value)
            elif direction == 7:
                set_pins_state({
                    out1: State.HIGH.value,
                    out2: State.LOW.value,
                    out3: State.LOW.value,
                    out4: State.HIGH.value
                }, BoardMode.BOARD.value)
            if direction == 0:
                direction = 7
            continue
        time.sleep(0.008)
        direction = direction - 1


if __name__ == '__main__':
    fixture_set = {
        Fixture("P1", {
            FixtureState.FREE: Pin.P13,
            FixtureState.ASSEMBLING: Pin.P19,
            FixtureState.COMPLETED: Pin.P26
        }), Fixture("P2", {
            FixtureState.FREE: Pin.P12,
            FixtureState.ASSEMBLING: Pin.P16,
            FixtureState.PENDING: Pin.P20,
            FixtureState.COMPLETED: Pin.P21
        }), Fixture("P3", {
            FixtureState.FREE: Pin.P15,
            FixtureState.ASSEMBLING: Pin.P5,
            FixtureState.COMPLETED: Pin.P6
        })
    }
    workbench_1 = Workbench("W1", fixture_set, workbench_rotate)
    try:
        init_pins()
        set_initial_state_for_fixtures(workbench_1)
        app = create_app(workbench_1)
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(e)
    finally:
        cleanup()
