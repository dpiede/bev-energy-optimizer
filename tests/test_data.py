from bev.data import tou_prices_jpy_per_kwh


def test_tou_prices_shape_and_bands():
    p = tou_prices_jpy_per_kwh()
    assert p.shape == (24,)
    assert p[3] < p[12] < p[18]  # night < day < peak


def test_tou_prices_start_hour_wraps():
    p = tou_prices_jpy_per_kwh(horizon_h=24, start_hour=18)
    assert p[0] == tou_prices_jpy_per_kwh()[18]
    assert p[6] == tou_prices_jpy_per_kwh()[0]
