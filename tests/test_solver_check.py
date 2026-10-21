import pytest

from bev.solver_check import solve_toy_lp


def test_toy_lp_solves_to_known_optimum():
    assert solve_toy_lp() == pytest.approx(3.0, abs=1e-6)
