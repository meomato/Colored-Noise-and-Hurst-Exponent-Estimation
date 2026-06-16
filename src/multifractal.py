"""Simple q-order fluctuation functions based on DFA windows."""

from __future__ import annotations

import numpy as np

from .estimators import make_scales


def q_order_fluctuations(
    series: np.ndarray,
    q_values: list[float] | np.ndarray | None = None,
    scales: np.ndarray | None = None,
    order: int = 1,
) -> dict[float, tuple[np.ndarray, np.ndarray]]:
    """Compute F_q(s) curves with a simple MFDFA-like procedure."""
    if q_values is None:
        q_values = [-4, -2, 0, 2, 4]
    x = np.asarray(series, dtype=float)
    if scales is None:
        scales = make_scales(len(x), min_scale=16, count=16)

    profile = np.cumsum(x - np.mean(x))
    output: dict[float, tuple[np.ndarray, np.ndarray]] = {}

    for q in q_values:
        used = []
        values = []
        for scale in scales:
            blocks = len(profile) // scale
            if blocks < 2:
                continue
            variances = []
            t = np.arange(scale)
            for block in range(blocks):
                part = profile[block * scale : (block + 1) * scale]
                coeffs = np.polyfit(t, part, deg=order)
                trend = np.polyval(coeffs, t)
                variance = np.mean((part - trend) ** 2)
                if variance > 0:
                    variances.append(variance)
            if not variances:
                continue
            variances = np.asarray(variances, dtype=float)
            if q == 0:
                fq = np.exp(0.5 * np.mean(np.log(variances)))
            else:
                fq = (np.mean(variances ** (q / 2.0))) ** (1.0 / q)
            used.append(scale)
            values.append(fq)
        output[float(q)] = (np.asarray(used, dtype=float), np.asarray(values, dtype=float))

    return output

