import typing
from enum import Enum

from enum import Enum


class Fixture(Enum):
    P1 = "P1"

    def __str__(self):
        return self.value


class FixtureState(Enum):
    FREE = "FREE"
    ASSEMBLING = "ASSEMBLING"
    PENDING = "PENDING"

    def __str__(self):
        return self.value


# Dictionary mapping fixtures to possible states
fixture_states = {
    Fixture.P1: {FixtureState.FREE, FixtureState.ASSEMBLING, FixtureState.PENDING}
}


def get_available_states_for_given_fixture(fixture: Fixture) -> typing.Set[FixtureState]:
    return fixture_states.get(fixture, set())
