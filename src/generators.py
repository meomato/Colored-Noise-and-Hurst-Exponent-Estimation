"""Generators for fractional Gaussian noise, fBm, colored noise, and fOU."""

from __future__ import annotations

import numpy as np
from fbm import FBM


def generate_fgn(n: int, hurst: float, length: float = 1.0, seed: int | None = None) -> np.ndarray:
    """Generate fractional Gaussian noise with the fbm package.

    The fbm package implements common fBm/fGn simulation methods, including
    Davies-Harte. fGn is used here as colored noise with a chosen Hurst exponent.
    """
    if seed is not None:
        np.random.seed(seed)
    model = FBM(n=n, hurst=hurst, length=length, method="daviesharte")
    values = np.asarray(model.fgn(), dtype=float)
    return standardize(values)


def generate_fbm(n: int, hurst: float, length: float = 1.0, seed: int | None = None) -> np.ndarray:
    """Generate a fractional Brownian motion sample path."""
    if seed is not None:
        np.random.seed(seed)
    model = FBM(n=n, hurst=hurst, length=length, method="daviesharte")
    values = np.asarray(model.fbm(), dtype=float)
    return values


def generate_fbm_from_fgn(n: int, hurst: float, seed: int | None = None) -> np.ndarray:
    """Generate fBm as a cumulative sum of fGn."""
    noise = generate_fgn(n=n, hurst=hurst, seed=seed)
    return np.concatenate([[0.0], np.cumsum(noise)])


def generate_fou(
    n: int,
    hurst: float,
    theta: float = 1.2,
    sigma: float = 0.8,
    dt: float = 1.0,
    x0: float = 0.0,
    seed: int | None = None,
) -> np.ndarray:
    """Generate a simple fractional Ornstein-Uhlenbeck path.

        X[t] = X[t-1] - theta * X[t-1] * dt + sigma * dB_H[t]

    The point is to show mean reversion combined with fractional noise.
    """
    increments = generate_fgn(n=n, hurst=hurst, seed=seed)
    x = np.zeros(n, dtype=float)
    x[0] = x0
    for t in range(1, n):
        drift = -theta * x[t - 1] * dt
        shock = sigma * (dt**hurst) * increments[t]
        x[t] = x[t - 1] + drift + shock
    return x


def generate_power_law_noise(n: int, beta: float, seed: int | None = None) -> np.ndarray:
    """Generate simple 1/f^beta colored noise in the frequency domain.

    This is included as an extra colored-noise example. It is not used as the
    main Hurst experiment, because fGn has a clearer relation beta = 2H - 1.
    """
    rng = np.random.default_rng(seed)
    white = rng.normal(size=n)
    spectrum = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n)
    weights = np.ones_like(freqs)
    weights[1:] = freqs[1:] ** (-beta / 2.0)
    colored = np.fft.irfft(spectrum * weights, n=n)
    return standardize(colored)


def generate_fgn_cholesky(n: int, hurst: float, seed: int | None = None) -> np.ndarray:
    """Small custom fGn generator using the covariance matrix and Cholesky.

    This method is slow for large n, so the experiment uses the fbm package.
    It is useful to show the covariance idea directly from the theory.
    """
    rng = np.random.default_rng(seed)
    gamma = np.fromfunction(
        lambda i, j: 0.5
        * (
            np.abs(i - j - 1) ** (2 * hurst)
            - 2 * np.abs(i - j) ** (2 * hurst)
            + np.abs(i - j + 1) ** (2 * hurst)
        ),
        (n, n),
        dtype=float,
    )
    gamma += np.eye(n) * 1e-10
    lower = np.linalg.cholesky(gamma)
    sample = lower @ rng.normal(size=n)
    return standardize(sample)


def standardize(values: np.ndarray) -> np.ndarray:
    """Return zero-mean, unit-variance data."""
    values = np.asarray(values, dtype=float)
    std = np.std(values)
    if std == 0:
        return values - np.mean(values)
    return (values - np.mean(values)) / std

