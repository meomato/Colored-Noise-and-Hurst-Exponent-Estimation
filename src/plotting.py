"""Plotting helpers for the colored noise project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save_sample_paths(paths: dict[float, np.ndarray], title: str, ylabel: str, filename: Path) -> None:
    fig, axes = plt.subplots(len(paths), 1, figsize=(9, 8), sharex=True)
    fig.suptitle(title)
    for ax, (hurst, values) in zip(axes, paths.items()):
        ax.plot(values, linewidth=1.0)
        ax.set_ylabel(f"H={hurst}")
        ax.grid(alpha=0.25)
    axes[-1].set_xlabel("time index")
    fig.text(0.03, 0.5, ylabel, rotation="vertical", va="center")
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def save_loglog_plot(scales: np.ndarray, values: np.ndarray, slope: float, title: str, ylabel: str, filename: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(scales, values, "o-", label="computed values")
    fit = np.exp(np.polyval(np.polyfit(np.log(scales), np.log(values), 1), np.log(scales)))
    ax.plot(scales, fit, "--", label=f"log-log slope = {slope:.3f}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("window size s")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def save_true_vs_estimated(summary: pd.DataFrame, filename: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    methods = list(summary["method"].unique())
    for method in methods:
        part = summary[summary["method"] == method]
        ax.plot(part["hurst_true"], part["estimate_mean"], "o-", label=method)
    xs = sorted(summary["hurst_true"].unique())
    ax.plot(xs, xs, "k--", label="ideal")
    ax.set_xlabel("true H")
    ax.set_ylabel("estimated H")
    ax.set_title("True H versus estimated H")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def save_error_plot(summary: pd.DataFrame, filename: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    methods = list(summary["method"].unique())
    for method in methods:
        part = summary[summary["method"] == method]
        ax.plot(part["hurst_true"], part["absolute_error"], "o-", label=method)
    ax.set_xlabel("true H")
    ax.set_ylabel("mean absolute error")
    ax.set_title("Estimation error by method")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def save_multifractal_plot(curves: dict[float, tuple[np.ndarray, np.ndarray]], title: str, filename: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    for q, (scales, values) in curves.items():
        if len(scales) > 0:
            ax.plot(scales, values, "o-", label=f"q={q:g}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("window size s")
    ax.set_ylabel("F_q(s)")
    ax.set_title(title)
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)

