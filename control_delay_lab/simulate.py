from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Parameters:
    dt_s: float = 0.005
    duration_s: float = 8.0
    setpoint: float = 1.0
    step_time_s: float = 0.1
    kp: float = 30.0
    ki: float = 0.5
    kd: float = 6.0
    inertia: float = 1.0
    damping: float = 2.0
    max_control: float = 50.0
    settling_band_pct: float = 2.0


def simulate(delay_ms: float, params: Parameters) -> tuple[list[dict[str, float]], dict[str, float | str]]:
    if params.dt_s <= 0 or params.duration_s <= 0 or params.inertia <= 0:
        raise ValueError("dt_s, duration_s, and inertia must be positive")
    total_steps = int(params.duration_s / params.dt_s) + 1
    delay_steps = round(delay_ms / (1000.0 * params.dt_s))
    command_queue = [0.0] * delay_steps
    position = velocity = integral = 0.0
    trace: list[dict[str, float]] = []
    target_reached = False
    peak_position = float("-inf")
    diverged = False
    for step in range(total_steps):
        time_s = step * params.dt_s
        setpoint = params.setpoint if time_s >= params.step_time_s else 0.0
        error = setpoint - position
        integral += error * params.dt_s
        control = max(-params.max_control, min(params.max_control, params.kp * error + params.ki * integral - params.kd * velocity))
        if delay_steps == 0:
            applied_control = control
        else:
            command_queue.append(control)
            applied_control = command_queue.pop(0)
        acceleration = (applied_control - params.damping * velocity) / params.inertia
        velocity += acceleration * params.dt_s
        position += velocity * params.dt_s
        if setpoint != 0:
            target_reached = True
            peak_position = max(peak_position, position)
        if abs(position) > 20 or abs(velocity) > 100:
            diverged = True
        trace.append({"time_s": time_s, "setpoint": setpoint, "position": position, "velocity": velocity, "control": applied_control})
        if diverged:
            break
    settling_time = _settling_time(trace, params)
    final_error = abs(params.setpoint - trace[-1]["position"]) if trace else abs(params.setpoint)
    overshoot_pct = max(0.0, (peak_position - params.setpoint) / abs(params.setpoint) * 100.0) if target_reached and params.setpoint else 0.0
    stability = "diverged" if diverged else ("settled" if settling_time is not None else "not_settled")
    summary: dict[str, float | str] = {
        "delay_ms": delay_ms, "overshoot_pct": overshoot_pct,
        "settling_time_s": round(settling_time, 3) if settling_time is not None else "not_reached",
        "final_error": final_error, "peak_position": peak_position if target_reached else 0.0,
        "stability": stability,
    }
    return trace, summary


def _settling_time(trace: list[dict[str, float]], params: Parameters) -> float | None:
    band = abs(params.setpoint) * params.settling_band_pct / 100.0
    step_index = next((i for i, row in enumerate(trace) if row["time_s"] >= params.step_time_s), None)
    if step_index is None:
        return None
    latest_out_of_band = step_index - 1
    for i in range(len(trace) - 1, step_index - 1, -1):
        if abs(trace[i]["position"] - params.setpoint) > band:
            latest_out_of_band = i
            break
    candidate = latest_out_of_band + 1
    if candidate < len(trace) and candidate >= step_index:
        return trace[candidate]["time_s"] - params.step_time_s
    if latest_out_of_band == step_index - 1:
        return trace[step_index]["time_s"] - params.step_time_s
    return None


def run_experiment(delays_ms: Iterable[float], params: Parameters) -> tuple[dict[float, list[dict[str, float]]], list[dict[str, float | str]]]:
    traces: dict[float, list[dict[str, float]]] = {}
    summaries: list[dict[str, float | str]] = []
    for delay_ms in delays_ms:
        trace, summary = simulate(float(delay_ms), params)
        traces[float(delay_ms)] = trace
        summaries.append(summary)
    return traces, summaries

