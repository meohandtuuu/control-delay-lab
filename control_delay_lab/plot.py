from __future__ import annotations

from html import escape
from pathlib import Path

COLORS = ["#1769aa", "#d1495b", "#2a9d8f", "#e09f3e", "#7353ba", "#4b5563"]


def write_svg(traces: dict[float, list[dict[str, float]]], path: Path) -> None:
    width, height = 960, 560
    left, right, top, bottom = 82, 25, 35, 75
    rows = [row for trace in traces.values() for row in trace]
    max_time = max((row["time_s"] for row in rows), default=1.0) or 1.0
    max_y = max((max(abs(row["position"]) for row in trace) for trace in traces.values() if trace), default=1.0)
    y_limit = max(1.2, min(5.0, max_y * 1.1))
    plot_w, plot_h = width - left - right, height - top - bottom
    x = lambda value: left + value / max_time * plot_w
    y = lambda value: top + (y_limit - value) / (2 * y_limit) * plot_h
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
              '<rect width="100%" height="100%" fill="#fff"/>',
              '<text x="480" y="24" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="700">PID step response by command delay</text>']
    for i in range(5):
        value = -y_limit + 2 * y_limit * i / 4
        yy = y(value)
        chunks.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#e5e7eb"/>')
        chunks.append(f'<text x="{left-10}" y="{yy+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="11" fill="#4b5563">{value:.1f}</text>')
    for i in range(5):
        value = max_time * i / 4
        xx = x(value)
        chunks.append(f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" stroke="#f1f3f5"/>')
        chunks.append(f'<text x="{xx:.1f}" y="{height-bottom+20}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#4b5563">{value:.1f}</text>')
    chunks.append(f'<line x1="{left}" y1="{y(1):.1f}" x2="{width-right}" y2="{y(1):.1f}" stroke="#111827" stroke-dasharray="5 4"/>')
    chunks.append(f'<text x="{width/2}" y="{height-20}" text-anchor="middle" font-family="sans-serif" font-size="13">Time (s)</text>')
    chunks.append(f'<text transform="translate(20 {height/2}) rotate(-90)" text-anchor="middle" font-family="sans-serif" font-size="13">Position (simulated units)</text>')
    for index, (delay_ms, trace) in enumerate(sorted(traces.items())):
        color = COLORS[index % len(COLORS)]
        points = " ".join(f'{x(row["time_s"]):.1f},{y(row["position"]):.1f}' for row in trace)
        chunks.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}"/>')
        lx, ly = left + 12 + (index % 3) * 155, top + 18 + (index // 3) * 20
        chunks.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+22}" y2="{ly}" stroke="{color}" stroke-width="3"/>')
        chunks.append(f'<text x="{lx+28}" y="{ly+4}" font-family="sans-serif" font-size="12" fill="#111827">{escape(str(delay_ms))} ms</text>')
    chunks.append('</svg>')
    path.write_text("\n".join(chunks), encoding="utf-8")

