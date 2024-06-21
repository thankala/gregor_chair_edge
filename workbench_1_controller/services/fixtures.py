from enum import Enum

import typing
from enum import Enum


class Fixture(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

    def __str__(self):
        return self.value


class FixtureState(Enum):
    FREE = "FREE"
    ASSEMBLING = "ASSEMBLING"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

    def __str__(self):
        return self.value


# Dictionary mapping fixtures to possible states
fixture_states = {
    Fixture.P1: {FixtureState.FREE, FixtureState.PENDING, FixtureState.COMPLETED},
    Fixture.P2: {FixtureState.FREE, FixtureState.ASSEMBLING, FixtureState.PENDING, FixtureState.COMPLETED},
    Fixture.P3: {FixtureState.FREE, FixtureState.ASSEMBLING, FixtureState.COMPLETED}
}


def get_available_states_for_given_fixture(fixture: Fixture) -> typing.Set[FixtureState]:
    return fixture_states.get(fixture, set())
