import numpy as np
import pytest

from bev.charging import optimise_charging
from bev.data import tou_prices_jpy_per_kwh

TOL = 1e-6

BATTERY_KWH = 60.0
CHARGER_KW = 6.0
EFFICIENCY = 0.95
SOC_INIT_KWH = 18.0  # 30%
DEPARTURE_STEP = 13  # 18:00 start -> 07:00
MIN_SOC_KWH = 0.20 * BATTERY_KWH
TARGET_SOC_KWH = 0.80 * BATTERY_KWH


@pytest.fixture
def scenario():
    prices = tou_prices_jpy_per_kwh(24, start_hour=18)
    plugged_in = np.array([1] * DEPARTURE_STEP + [0] * (24 - DEPARTURE_STEP))
    return prices, plugged_in


@pytest.fixture
def result(scenario):
    prices, plugged_in = scenario
    return optimise_charging(prices, plugged_in, SOC_INIT_KWH, DEPARTURE_STEP)


def test_status_optimal(result):
    assert result.status == "optimal"


def test_array_lengths(result):
    assert len(result.charge_kw) == 24
    assert len(result.soc_kwh) == 25


def test_starts_at_initial_soc(result):
    assert result.soc_kwh[0] == pytest.approx(SOC_INIT_KWH, abs=TOL)


def test_soc_within_bounds(result):
    assert result.soc_kwh.min() >= MIN_SOC_KWH - TOL
    assert result.soc_kwh.max() <= BATTERY_KWH + TOL


def test_target_reached_at_departure(result):
    assert result.soc_kwh[DEPARTURE_STEP] >= TARGET_SOC_KWH - TOL


def test_power_limits(result):
    assert result.charge_kw.min() >= -TOL
    assert result.charge_kw.max() <= CHARGER_KW + TOL


def test_no_charging_when_unplugged(scenario, result):
    _, plugged_in = scenario
    assert np.all(result.charge_kw[plugged_in == 0] <= TOL)


def test_soc_follows_energy_balance(result):
    expected = result.soc_kwh[:-1] + EFFICIENCY * result.charge_kw
    assert result.soc_kwh[1:] == pytest.approx(expected, abs=TOL)


def test_cost_matches_hand_calculation(result):
    # (48 - 18) kWh into the battery / 0.95 efficiency, all at night price 25 JPY/kWh
    expected_jpy = (TARGET_SOC_KWH - SOC_INIT_KWH) / EFFICIENCY * 25.0
    assert result.cost_jpy == pytest.approx(expected_jpy, abs=1e-4)


def test_charges_only_in_cheapest_hours(scenario, result):
    prices, _ = scenario
    charging = result.charge_kw > TOL
    assert np.all(prices[charging] == prices.min())


def test_infeasible_target_raises(scenario):
    prices, plugged_in = scenario
    # 2 plugged-in hours at 6 kW cannot add 30 kWh
    short_stay = np.array([1, 1] + [0] * 22)
    with pytest.raises(ValueError):
        optimise_charging(prices, short_stay, SOC_INIT_KWH, departure_step=2)
