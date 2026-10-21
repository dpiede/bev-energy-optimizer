# BEV Energy Optimizer

Optimising when a battery electric vehicle charges and discharges (vehicle-to-home, V2H)
to minimise household electricity cost, using forecasts as inputs.

Built with Python, [CVXPY](https://www.cvxpy.org/) and [uv](https://docs.astral.sh/uv/).
All data is synthetic.

## Quickstart

```bash
uv sync
uv run python -m bev.solver_check
uv run pytest
```

## Roadmap

1. Smart charging: reach target SoC by departure at minimum cost (LP)
2. V2H: car supplies house load, with round-trip losses and degradation cost
3. Uncertain departure time: plan against a conservative quantile
4. Rolling horizon (MPC) over one week
5. Benchmark against naive "charge on arrival"
