"""Manual Hurst exponent estimators and optional library comparison."""

from __future__ import annotations

import numpy as np
from scipy.stats import linregress

_NOLDS_MODULE = None
_NOLDS_CHECKED = False


def make_scales(n: int, min_scale: int = 16, max_scale: int | None = None, count: int = 18) -> np.ndarray:
    """Create unique logarithmic window sizes."""
    if max_scale is None:
        max_scale = n // 4
    raw = np.logspace(np.log10(min_scale), np.log10(max_scale), count)
    scales = np.unique(raw.astype(int))
    return scales[scales >= 4]


def estimate_hurst_rs(series: np.ndarray, scales: np.ndarray | None = None) -> tuple[float, np.ndarray, np.ndarray]:
    """Estimate H with rescaled range analysis."""
    x = np.asarray(series, dtype=float)
    if scales is None:
        scales = make_scales(len(x))

    rs_values = []
    used_scales = []
    for scale in scales:
        blocks = len(x) // scale
        if blocks < 2:
            continue
        values = []
        for block in range(blocks):
            part = x[block * scale : (block + 1) * scale]
            centered = part - np.mean(part)
            cumulative = np.cumsum(centered)
            r_value = np.max(cumulative) - np.min(cumulative)
            s_value = np.std(part, ddof=1)
            if s_value > 0:
                values.append(r_value / s_value)
        if values:
            used_scales.append(scale)
            rs_values.append(np.mean(values))

    used_scales = np.asarray(used_scales, dtype=float)
    rs_values = np.asarray(rs_values, dtype=float)
    slope, _, _, _, _ = linregress(np.log(used_scales), np.log(rs_values))
    return float(slope), used_scales, rs_values


def estimate_hurst_dfa(
    series: np.ndarray,
    scales: np.ndarray | None = None,
    order: int = 1,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Estimate H with detrended fluctuation analysis."""
    x = np.asarray(series, dtype=float)
    if scales is None:
        scales = make_scales(len(x))

    profile = np.cumsum(x - np.mean(x))
    flucts = []
    used_scales = []
    for scale in scales:
        blocks = len(profile) // scale
        if blocks < 2:
            continue
        rms_values = []
        t = np.arange(scale)
        for block in range(blocks):
            part = profile[block * scale : (block + 1) * scale]
            coeffs = np.polyfit(t, part, deg=order)
            trend = np.polyval(coeffs, t)
            rms = np.sqrt(np.mean((part - trend) ** 2))
            if rms > 0:
                rms_values.append(rms)
        if rms_values:
            used_scales.append(scale)
            flucts.append(np.sqrt(np.mean(np.asarray(rms_values) ** 2)))

    used_scales = np.asarray(used_scales, dtype=float)
    flucts = np.asarray(flucts, dtype=float)
    slope, _, _, _, _ = linregress(np.log(used_scales), np.log(flucts))
    return float(slope), used_scales, flucts


def try_nolds_estimates(series: np.ndarray) -> dict[str, float]:
    """Return nolds estimates when the local package import works."""
    module = _load_nolds_module()
    if module is None:
        return {"nolds_rs": np.nan, "nolds_dfa": np.nan}
    try:
        return {
            "nolds_rs": float(module.hurst_rs(series, fit="poly")),
            "nolds_dfa": float(module.dfa(series, fit_exp="poly")),
        }
    except Exception:
        return {"nolds_rs": np.nan, "nolds_dfa": np.nan}


def _load_nolds_module():
    global _NOLDS_MODULE, _NOLDS_CHECKED
    if _NOLDS_CHECKED:
        return _NOLDS_MODULE

    _NOLDS_CHECKED = True
    try:
        import nolds

        _NOLDS_MODULE = nolds
        return _NOLDS_MODULE
    except Exception:
        pass

    try:
        import importlib.util
        import site
        from pathlib import Path

        for base in site.getsitepackages():
            candidate = Path(base) / "nolds" / "measures.py"
            if candidate.exists():
                spec = importlib.util.spec_from_file_location("nolds_measures_local", candidate)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    _NOLDS_MODULE = module
                    return _NOLDS_MODULE
    except Exception:
        return None

    return None


def estimate_all(series: np.ndarray, include_nolds: bool = True) -> dict[str, float]:
    """Estimate H with custom methods and optional nolds methods."""
    rs_h, _, _ = estimate_hurst_rs(series)
    dfa_h, _, _ = estimate_hurst_dfa(series)
    estimates = {"custom_rs": rs_h, "custom_dfa": dfa_h}
    if include_nolds:
        estimates.update(try_nolds_estimates(series))
    return estimates
