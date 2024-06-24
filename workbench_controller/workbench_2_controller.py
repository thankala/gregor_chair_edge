import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workbench_controller.controllers.controller import create_app
from workbench_controller.services.service import cleanup, init_pins, set_initial_state_for_fixtures
from workbench_controller.domain.pins import Pins
from workbench_controller.domain.workbench import Workbench, Fixture, FixtureState

if __name__ == '__main__':
    fixture_set = {
        Fixture("P1", {
            FixtureState.FREE: Pins.P14,
            FixtureState.ASSEMBLING: Pins.P15,
            FixtureState.PENDING: Pins.P18
        })
    }
    workbench_2 = Workbench("W2", fixture_set)
    try:
        init_pins(workbench_2)
        set_initial_state_for_fixtures(workbench_2)
        app = create_app(workbench_2)
        app.run(host='0.0.0.0', port=5000)
    finally:
        cleanup(workbench_2)
