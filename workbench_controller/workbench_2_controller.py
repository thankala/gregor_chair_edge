from controllers.controller import create_app
from services.service import cleanup, init_pins, set_initial_state_for_fixtures
from domain.pin import Pin
from domain.workbench import Workbench, Fixture, FixtureState

if __name__ == '__main__':
    fixture_set = {
        Fixture("P1", {
            FixtureState.FREE: Pin.P14,
            FixtureState.ASSEMBLING: Pin.P15,
            FixtureState.PENDING: Pin.P18
        })
    }
    workbench_2 = Workbench("W2", fixture_set)
    try:
        init_pins()
        set_initial_state_for_fixtures(workbench_2)
        app = create_app(workbench_2)
        app.run(host='0.0.0.0', port=5000)
    finally:
        cleanup()
