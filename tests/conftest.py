import pytest

from crnstudio import DeterministicSimulator


@pytest.fixture
def setup_simulator() -> DeterministicSimulator:
    return DeterministicSimulator()
