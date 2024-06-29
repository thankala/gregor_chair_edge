import time

from domain.state import State
from controllers.controller import create_app
from services.service import cleanup, init_pins, set_initial_state_for_fixtures, gpio_set_pin_state
from domain.pin import Pin
from domain.workbench import Workbench, Fixture, FixtureState

out1 = Pin.P27
out2 = Pin.P17
out3 = Pin.P22
out4 = Pin.P18


def workbench_rotate() -> None:
    direction = 2
    for item in range(1):
        for step in range(129, 0, -1):
            if direction == 0:
                gpio_set_pin_state(out1.value, State.HIGH.value)
                gpio_set_pin_state(out2.value, State.LOW.value)
                gpio_set_pin_state(out3.value, State.LOW.value)
                gpio_set_pin_state(out4.value, State.LOW.value)
                time.sleep(0.008)
            elif direction == 1:
                gpio_set_pin_state(out1.value, State.HIGH.value)
                gpio_set_pin_state(out2.value, State.HIGH.value)
                gpio_set_pin_state(out3.value, State.LOW.value)
                gpio_set_pin_state(out4.value, State.LOW.value)
                time.sleep(0.008)
            elif direction == 2:
                gpio_set_pin_state(out1.value, State.LOW.value)
                gpio_set_pin_state(out2.value, State.HIGH.value)
                gpio_set_pin_state(out3.value, State.LOW.value)
                gpio_set_pin_state(out4.value, State.LOW.value)
                time.sleep(0.008)
            elif direction == 3:
                gpio_set_pin_state(out1.value, State.LOW.value)
                gpio_set_pin_state(out2.value, State.HIGH.value)
                gpio_set_pin_state(out3.value, State.HIGH.value)
                gpio_set_pin_state(out4.value, State.LOW.value)
                time.sleep(0.008)
            elif direction == 4:
                gpio_set_pin_state(out1.value, State.LOW.value)
                gpio_set_pin_state(out2.value, State.LOW.value)
                gpio_set_pin_state(out3.value, State.HIGH.value)
                gpio_set_pin_state(out4.value, State.LOW.value)
                time.sleep(0.008)
            elif direction == 5:
                gpio_set_pin_state(out1.value, State.LOW.value)
                gpio_set_pin_state(out2.value, State.LOW.value)
                gpio_set_pin_state(out3.value, State.HIGH.value)
                gpio_set_pin_state(out4.value, State.HIGH.value)
                time.sleep(0.008)
            elif direction == 6:
                gpio_set_pin_state(out1.value, State.LOW.value)
                gpio_set_pin_state(out2.value, State.LOW.value)
                gpio_set_pin_state(out3.value, State.LOW.value)
                gpio_set_pin_state(out4.value, State.HIGH.value)
                time.sleep(0.008)
            elif direction == 7:
                gpio_set_pin_state(out1.value, State.HIGH.value)
                gpio_set_pin_state(out2.value, State.LOW.value)
                gpio_set_pin_state(out3.value, State.LOW.value)
                gpio_set_pin_state(out4.value, State.HIGH.value)
                time.sleep(0.008)
            if direction == 0:
                direction = 7
                continue
            direction = direction - 1
    cleanup({out1, out2, out3, out4})


if __name__ == '__main__':
    fixture_set = {
        Fixture("F1", {
            FixtureState.FREE: Pin.P13,
            FixtureState.ASSEMBLING: Pin.P19,
            FixtureState.COMPLETED: Pin.P26
        }), Fixture("F2", {
            FixtureState.FREE: Pin.P12,
            FixtureState.ASSEMBLING: Pin.P16,
            FixtureState.PENDING: Pin.P20,
            FixtureState.COMPLETED: Pin.P21
        }), Fixture("F3", {
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
