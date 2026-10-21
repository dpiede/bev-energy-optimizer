"""Synthetic input data (prices, loads). All randomness is seeded."""

import numpy as np

# Japanese-style time-of-use tariff, JPY/kWh, by hour of day.
TOU_NIGHT_JPY_PER_KWH = 25.0  # 23:00-07:00
TOU_DAY_JPY_PER_KWH = 35.0  # 07:00-17:00, 21:00-23:00
TOU_PEAK_JPY_PER_KWH = 45.0  # 17:00-21:00


def tou_prices_jpy_per_kwh(horizon_h: int = 24, start_hour: int = 0) -> np.ndarray:
    """Hourly time-of-use prices starting at `start_hour` (0-23)."""
    hours = (start_hour + np.arange(horizon_h)) % 24
    prices = np.full(horizon_h, TOU_DAY_JPY_PER_KWH)
    prices[(hours >= 23) | (hours < 7)] = TOU_NIGHT_JPY_PER_KWH
    prices[(hours >= 17) & (hours < 21)] = TOU_PEAK_JPY_PER_KWH
    return prices
