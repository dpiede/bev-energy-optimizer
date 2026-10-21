from dataclasses import dataclass

import cvxpy as cp
import numpy as np


@dataclass
class ChargingResult:
    charge_kw: np.ndarray
    soc_kwh: np.ndarray
    cost_jpy: float
    status: str


def optimise_charging(
    price_jpy_per_kwh: np.ndarray,
    plugged_in: np.ndarray,
    soc_init_kwh: float,
    departure_step: int,
    battery_kwh: float = 60.0,
    charger_kw: float = 6.0,
    efficiency: float = 0.95,
    min_soc_frac: float = 0.20,
    target_soc_frac: float = 0.80,
) -> ChargingResult:
    len_horizon = len(price_jpy_per_kwh) 
    charge_kw = cp.Variable(len_horizon) # Decision Variable
    soc_kwh = cp.Variable(len_horizon + 1) # Decision Variable
    
    constraints = [] 
    for t in range(len_horizon):
        constraints.append(soc_kwh[t+1] == soc_kwh[t] + charge_kw[t] * efficiency) # Lock formula to track charge status
        
    constraints.append(soc_kwh[departure_step] >= target_soc_frac * battery_kwh) # At departure target kWh must be reached at minimum
    constraints.append(soc_kwh[0] == soc_init_kwh) # first step is init amount
    constraints.append(soc_kwh <= battery_kwh) # cannot exceed battery capacity
    constraints.append(soc_kwh >= min_soc_frac * battery_kwh) # cannot be lower than minimum capacity set
    constraints.append(charge_kw <= charger_kw * plugged_in) # Only charge when plugged in, up to charger max power
    constraints.append(charge_kw >= 0) # No negative charge allowed
    
    
    problem = cp.Problem(cp.Minimize(price_jpy_per_kwh @ charge_kw), constraints)
    problem.solve()
    
    if problem.status in ["infeasible", "infeasible_inaccurate"]:   
        raise ValueError("Cannot optimize, problem infeasible.")
    
    return ChargingResult(charge_kw.value, soc_kwh.value, problem.value, problem.status)
    