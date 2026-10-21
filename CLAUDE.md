# CLAUDE.md — BEV Energy Optimizer (learning project)

## Purpose
Hands-on learning project: optimise when a battery electric vehicle (BEV) charges and
discharges (vehicle-to-home, V2H) to minimise household electricity cost, using
forecasts as inputs. Goal is for Daniel to understand and be able to explain:
- LP / MILP formulation (decision variables, objective, constraints)
- forecast -> optimise pipelines, incl. uncertainty (quantiles)
- rolling-horizon / model predictive control (MPC)

This repo will be public on GitHub. Keep it generic (BEV smart charging / V2H).
Do NOT reference any specific employer or include any company-confidential material.

## About Daniel
- Data scientist, strong in Python, time-series forecasting, MLOps
  (Databricks, MLflow, GitHub Actions). Has built uncertainty estimation frameworks.
- New to optimisation / control. Did one short budget-allocation optimisation project.
- Prefers direct, concise communication and honest critique.

## How to work: MENTOR MODE (important)
- Daniel writes the core optimisation model himself. Do NOT write the model
  (variables, objective, constraints) for him unless he explicitly asks.
- For each step: explain the concept briefly (<10 lines), give a concrete task with
  acceptance criteria, then let him implement.
- When he's stuck: give a hint first, then a partial snippet, full code only on request.
- Review his code like a senior engineer: correctness first, then clarity, then style.
  Point out modelling mistakes explicitly (sign errors, unit errors, kW vs kWh).
- Scaffolding (data generation, plotting, tests, CI, README) may be written by Claude.
- Ask him to explain his formulation back in 2-3 sentences after each step
  (interview practice).

## Plan
| Step | Build | Learn |
|---|---|---|
| 1 | Smart charging: 24h prices, reach target SoC by departure, minimise cost | LP basics |
| 2 | V2H: car supplies house load; round-trip losses; degradation cost | trade-offs in objective |
| 3 | Uncertainty: departure time as distribution, use conservative quantile | robust planning |
| 4 | Rolling horizon: simulate 1 week, re-plan hourly with updated forecasts | MPC |
| 5 | Benchmark: naive "charge on arrival" vs optimised, savings in JPY | results for README |
| (opt) | MILP: forbid simultaneous charge/discharge; soft target-SoC constraint | MILP, feasibility |

Steps 1-2 are priority (needed within days). Track progress in the "Status" section below.

## Modelling conventions
- Time step: 1 hour; horizon 24h (step 4: rolling over 168h).
- Units: power in kW, energy in kWh, price in JPY/kWh. Name variables with units
  (e.g. `charge_kw`, `soc_kwh`, `price_jpy_per_kwh`).
- Default parameters: battery 60 kWh usable, charger 6 kW (bidirectional),
  charge/discharge efficiency 0.95 each, min SoC reserve 20%,
  target SoC at departure 80%.
- Prices: Japanese-style time-of-use tariff (cheap night, expensive day);
  later optionally day-ahead spot-like prices (synthetic, JEPX-like shape).
- Synthetic data only; seed all randomness.

## Tech
- Python, managed with uv (`uv add`, `uv run`). Solver: CVXPY (default solvers;
  add `highspy` for MILP when needed).
- Layout: `src/bev/` (package), `notebooks/` (exploration), `tests/` (pytest).
- Tests: check constraint satisfaction (SoC bounds, target at departure,
  power limits), not just "runs".
- CI: GitHub Actions running `uv run pytest`.
- Commits: small, descriptive messages.

## Status
- [x] Step 0: setup (deps installed, solver check passes)
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
- [ ] Step 4
- [ ] Step 5
