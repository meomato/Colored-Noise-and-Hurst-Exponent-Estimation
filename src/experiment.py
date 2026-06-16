"""Run experiments comparing Hurst exponent estimators."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .estimators import estimate_all, estimate_hurst_dfa, estimate_hurst_rs
from .generators import generate_fbm, generate_fgn, generate_fou
from .multifractal import q_order_fluctuations
from .plotting import (
    save_error_plot,
    save_loglog_plot,
    save_multifractal_plot,
    save_sample_paths,
    save_true_vs_estimated,
)


@dataclass
class ExperimentConfig:
    n: int = 4096
    repeats: int = 100
    library_repeats: int = 20
    seed: int = 42
    hurst_values: tuple[float, ...] = (0.3, 0.5, 0.7, 0.9)


def run_experiment(config: ExperimentConfig, base_dir: Path) -> pd.DataFrame:
    """Run the full experiment and save tables and figures."""
    figures_dir = base_dir / "results" / "figures"
    tables_dir = base_dir / "results" / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    sample_fgn = {}
    sample_fbm = {}
    sample_fou = {}
    rows = []

    for h_index, hurst in enumerate(config.hurst_values):
        seed = config.seed + h_index * 1000
        sample_fgn[hurst] = generate_fgn(config.n, hurst, seed=seed)
        sample_fbm[hurst] = generate_fbm(config.n, hurst, seed=seed)
        sample_fou[hurst] = generate_fou(config.n, hurst, seed=seed)

        for repeat in range(config.repeats):
            local_seed = config.seed + h_index * 1000 + repeat
            series = generate_fgn(config.n, hurst, seed=local_seed)
            estimates = estimate_all(series, include_nolds=repeat < config.library_repeats)
            acf1 = float(sm.tsa.acf(series, nlags=1, fft=True)[1])
            for method, estimate in estimates.items():
                rows.append(
                    {
                        "process": "fGn",
                        "hurst_true": hurst,
                        "repeat": repeat,
                        "method": method,
                        "estimate": estimate,
                        "lag1_acf": acf1,
                    }
                )

    estimates_df = pd.DataFrame(rows)
    estimates_df.to_csv(tables_dir / "hurst_estimates_raw.csv", index=False)

    summary = (
        estimates_df.dropna(subset=["estimate"])
        .groupby(["process", "hurst_true", "method"], as_index=False)
        .agg(
            estimate_mean=("estimate", "mean"),
            estimate_std=("estimate", "std"),
            estimate_count=("estimate", "count"),
            lag1_acf_mean=("lag1_acf", "mean"),
        )
    )
    summary["absolute_error"] = np.abs(summary["estimate_mean"] - summary["hurst_true"])
    summary.to_csv(tables_dir / "hurst_estimates.csv", index=False)

    save_sample_paths(sample_fgn, "Fractional Gaussian noise sample paths", "fGn value", figures_dir / "01_fgn_sample_paths.png")
    save_sample_paths(sample_fbm, "Fractional Brownian motion sample paths", "fBm value", figures_dir / "02_fbm_sample_paths.png")
    save_sample_paths(sample_fou, "Fractional Ornstein-Uhlenbeck sample paths", "fOU value", figures_dir / "03_fou_sample_paths.png")

    demo_h = 0.7
    demo_series = sample_fgn[demo_h]
    rs_h, rs_scales, rs_values = estimate_hurst_rs(demo_series)
    dfa_h, dfa_scales, dfa_values = estimate_hurst_dfa(demo_series)
    save_loglog_plot(rs_scales, rs_values, rs_h, "R/S scaling for fGn with H=0.7", "mean R/S", figures_dir / "04_rs_loglog.png")
    save_loglog_plot(dfa_scales, dfa_values, dfa_h, "DFA scaling for fGn with H=0.7", "F(s)", figures_dir / "05_dfa_loglog.png")

    save_true_vs_estimated(summary, figures_dir / "06_true_vs_estimated_h.png")
    save_error_plot(summary, figures_dir / "07_estimation_error.png")

    curves = q_order_fluctuations(demo_series)
    save_multifractal_plot(curves, "q-order fluctuation curves for fGn with H=0.7", figures_dir / "08_multifractal_fluctuations.png")

    return summary
