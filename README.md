# Control Delay Lab

[中文说明](README.zh-CN.md)

Measure how command delay changes a PID controlled motor's step response.

This repository is a reproducible **simulation starter**. It creates CSV measurements and an SVG chart without external Python packages. Simulation results are not hardware measurements; replace the plant adapter with encoder readings before presenting results as real-world data.

## Quick start

```bash
python -m control_delay_lab --delays-ms 0,50,100,150,200 --out results
```

The command writes `results.csv`, `summary.json`, and `response.svg` under `results/`. The summary reports overshoot, settling time, final error, peak position, and a transparent stability label.

## What's included

- `control_delay_lab/simulate.py`: discrete-time PID and second-order plant model.
- `control_delay_lab/plot.py`: dependency-free SVG response plot.
- `docs/hardware-adapter.md`: plan for swapping the simulator for a motor and encoder.

## Model and limits

The simulated plant uses position, velocity, inertia, damping, actuator saturation, a fixed time step, and a FIFO command-delay queue. Default parameters are illustrative, not identified from a particular motor. Results depend on those parameters and must not be described as hardware evidence.

Python 3.10 or later; no third-party packages required. The CLI records all parameters in `summary.json`. Keep raw CSV output with plots you publish.

## License

MIT. See `LICENSE`.

