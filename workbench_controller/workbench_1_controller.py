import os, sys
import time

from workbench_controller.domain.board_mode import BoardMode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workbench_controller.domain.states import States
from workbench_controller.services.gpio import set_pins_state
from workbench_controller.controllers.controller import create_app
from workbench_controller.services.service import cleanup, init_pins, set_initial_state_for_fixtures
from workbench_controller.domain.pins import Pins
from workbench_controller.domain.workbench import Workbench, Fixture, FixtureState

out1 = Pins.P13.value
out2 = Pins.P11.value
out3 = Pins.P15.value
out4 = Pins.P12.value


def workbench_rotate() -> None:
    direction = 2
    for item in range(1):
        for Step in range(130, 0, -1):
            if direction == 0:
                set_pins_state({
                    out1: States.HIGH.value,
                    out2: States.LOW.value,
                    out3: States.LOW.value,
                    out4: States.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 1:
                set_pins_state({
                    out1: States.HIGH.value,
                    out2: States.HIGH.value,
                    out3: States.LOW.value,
                    out4: States.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 2:
                set_pins_state({
                    out1: States.LOW.value,
                    out2: States.HIGH.value,
                    out3: States.LOW.value,
                    out4: States.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 3:
                set_pins_state({
                    out1: States.LOW.value,
                    out2: States.HIGH.value,
                    out3: States.HIGH.value,
                    out4: States.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 4:
                set_pins_state({
                    out1: States.LOW.value,
                    out2: States.LOW.value,
                    out3: States.HIGH.value,
                    out4: States.LOW.value
                }, BoardMode.BOARD.value)
            elif direction == 5:
                set_pins_state({
                    out1: States.LOW.value,
                    out2: States.LOW.value,
                    out3: States.HIGH.value,
                    out4: States.HIGH.value
                }, BoardMode.BOARD.value)
            elif direction == 6:
                set_pins_state({
                    out1: States.LOW.value,
                    out2: States.LOW.value,
                    out3: States.LOW.value,
                    out4: States.HIGH.value
                }, BoardMode.BOARD.value)
            elif direction == 7:
                set_pins_state({
                    out1: States.HIGH.value,
                    out2: States.LOW.value,
                    out3: States.LOW.value,
                    out4: States.HIGH.value
                }, BoardMode.BOARD.value)
            if direction == 0:
                direction = 7
            continue
        time.sleep(0.008)
        direction = direction - 1


if __name__ == '__main__':
    fixture_set = {
        Fixture("P1", {
            FixtureState.FREE: Pins.P13,
            FixtureState.ASSEMBLING: Pins.P19,
            FixtureState.COMPLETED: Pins.P26
        }), Fixture("P2", {
            FixtureState.FREE: Pins.P12,
            FixtureState.ASSEMBLING: Pins.P16,
            FixtureState.PENDING: Pins.P20,
            FixtureState.COMPLETED: Pins.P21
        }), Fixture("P3", {
            FixtureState.FREE: Pins.P15,
            FixtureState.ASSEMBLING: Pins.P5,
            FixtureState.COMPLETED: Pins.P6
        })
    }
    workbench_1 = Workbench("W1", fixture_set, workbench_rotate)
    try:
        init_pins()
        set_initial_state_for_fixtures(workbench_1)
        app = create_app(workbench_1)
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(e)
    finally:
        cleanup()
