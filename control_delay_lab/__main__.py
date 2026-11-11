from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .plot import write_svg
from .simulate import Parameters, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a reproducible PID delay sweep.")
    parser.add_argument("--delays-ms", default="0,50,100,150,200", help="Comma-separated command delays")
    parser.add_argument("--out", default="results", help="Output directory")
    parser.add_argument("--duration-s", type=float, default=8.0)
    parser.add_argument("--dt-s", type=float, default=0.005)
    parser.add_argument("--kp", type=float, default=30.0)
    parser.add_argument("--ki", type=float, default=0.5)
    parser.add_argument("--kd", type=float, default=6.0)
    args = parser.parse_args()
    try:
        delays = [float(value.strip()) for value in args.delays_ms.split(",") if value.strip()]
        if not delays or any(value < 0 for value in delays):
            raise ValueError
    except ValueError:
        parser.error("--delays-ms must contain non-negative numbers")

    params = Parameters(dt_s=args.dt_s, duration_s=args.duration_s, kp=args.kp, ki=args.ki, kd=args.kd)
    traces, summaries = run_experiment(delays, params)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["delay_ms", "time_s", "setpoint", "position", "velocity", "control"])
        writer.writeheader()
        for delay_ms, trace in traces.items():
            for row in trace:
                writer.writerow({"delay_ms": delay_ms, **row})
    payload = {
        "evidence_type": "simulation",
        "model": "second_order_position_plant_with_delayed_command_queue",
        "parameters": {"dt_s": params.dt_s, "duration_s": params.duration_s, "setpoint": params.setpoint,
                       "step_time_s": params.step_time_s, "kp": params.kp, "ki": params.ki, "kd": params.kd,
                       "inertia": params.inertia, "damping": params.damping, "max_control": params.max_control,
                       "settling_band_pct": params.settling_band_pct, "delays_ms": delays},
        "runs": summaries,
    }
    (out_dir / "summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_svg(traces, out_dir / "response.svg")
    print(f"Wrote {len(summaries)} runs to {out_dir.resolve()}")
    for row in summaries:
        print(f"{row['delay_ms']:>6.1f} ms  {row['stability']:<14} overshoot={row['overshoot_pct']:>7.2f}%  settling={row['settling_time_s']}")


if __name__ == "__main__":
    main()

