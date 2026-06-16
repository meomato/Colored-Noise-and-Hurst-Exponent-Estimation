# Models: fBm, fGn, fOU, and ARFIMA

## 1. Fractional Brownian motion

Fractional Brownian motion is usually denoted by `B_H(t)`, where `H` is the
Hurst exponent. It generalizes ordinary Brownian motion. The special case
`H = 0.5` corresponds to classical Brownian motion.

The process is Gaussian and has zero mean:

```text
E[B_H(t)] = 0
```

Its covariance function is:

```text
E[B_H(t) B_H(s)] =
0.5 * (|t|^(2H) + |s|^(2H) - |t - s|^(2H))
```

Important properties:

- Gaussian distribution of finite-dimensional vectors;
- self-similarity with parameter `H`;
- stationary increments;
- nonstationarity of the process itself;
- roughness controlled by `H`.

Self-similarity means:

```text
B_H(a t) has the same distribution as a^H B_H(t)
```

Interpretation of `H`:

- small `H` gives rougher and more irregular paths;
- large `H` gives smoother paths;
- `H = 0.5` is the ordinary Brownian reference case.

In this project, fBm is generated mainly for visualization. The figure
`02_fbm_sample_paths.png` should show that paths become visually smoother when
`H` increases.

Code connection:

- function: `generate_fbm`
- file: `src/generators.py`
- source idea: Mandelbrot and Van Ness (1968)
- library used: `fbm.FBM(...).fbm()`

## 2. Fractional Gaussian noise

Fractional Gaussian noise is the increment process of fBm:

```text
X(t) = B_H(t + 1) - B_H(t)
```

Unlike fBm, fGn is stationary. This makes it more convenient for numerical
experiments with Hurst exponent estimation. The estimators in this project are
applied mainly to fGn, because estimating `H` from stationary increments is
more stable than estimating from the nonstationary fBm path.

For fGn, the autocorrelation structure depends on `H`:

- `H < 0.5`: increments tend to alternate direction;
- `H = 0.5`: increments are approximately uncorrelated;
- `H > 0.5`: increments show persistence.

For spectral color, the approximate relation is:

```text
beta = 2H - 1
```

Thus fGn can represent different colored-noise regimes:

```text
H = 0.3 -> beta = -0.4
H = 0.5 -> beta = 0.0
H = 0.7 -> beta = 0.4
H = 0.9 -> beta = 0.8
```

Code connection:

- function: `generate_fgn`
- file: `src/generators.py`
- source idea: fGn as increments of fBm
- library used: `fbm.FBM(...).fgn()`
- simulation method requested from the package: `daviesharte`

The project also includes a small custom Cholesky-based fGn generator:

- function: `generate_fgn_cholesky`
- purpose: demonstrate the covariance-matrix idea;
- limitation: slow for large samples, so it is not the main experiment method.

## 3. Davies-Harte and Cholesky simulation ideas

The code uses the `fbm` package for efficient generation. The package supports
standard fBm/fGn simulation methods such as Davies-Harte. The reason for using
the package is practical: for `n = 4096` and many realizations, direct covariance
matrix simulation would be slow.

The custom Cholesky idea is:

1. build the covariance matrix of fGn increments;
2. compute its Cholesky factor;
3. multiply this factor by a vector of independent standard normal variables.

This corresponds to the general Gaussian simulation principle:

```text
If Z ~ N(0, I), then LZ ~ N(0, LL^T)
```

where `LL^T` is the target covariance matrix.

This is useful for explanation, while the `fbm` package is better for the full
experiment.

## 4. Fractional Ornstein-Uhlenbeck process

The classical Ornstein-Uhlenbeck process is a mean-reverting stochastic process.
A simplified form is:

```text
dX_t = -theta * X_t dt + sigma dW_t
```

The drift term `-theta * X_t` pulls the process back toward zero. If a long-term
mean `mu` is included, the drift is often written as:

```text
theta * (mu - X_t) dt
```

The fractional version replaces the ordinary Brownian noise by a fractional
driver:

```text
dX_t = -theta * X_t dt + sigma dB_H(t)
```

In the code, this is implemented in discrete form:

```text
X[t] = X[t-1] - theta * X[t-1] * dt + sigma * dB_H[t]
```

where `dB_H[t]` is represented by fGn.

Parameters:

- `theta`: strength of mean reversion;
- `sigma`: size of the random shock;
- `H`: Hurst exponent of the fractional driver;
- `dt`: time step;
- `x0`: starting value.

Expected visual behavior:

- the path fluctuates around a central level;
- it does not drift away like fBm;
- larger `H` creates more persistent movement in the driving noise.

Code connection:

- function: `generate_fou`
- file: `src/generators.py`
- source idea: Ornstein-Uhlenbeck mean reversion plus fractional noise
- literature: Cheridito, Kawaguchi, and Maejima (2003)

This implementation is intentionally student-level. It is suitable for showing
the process numerically, but it is not presented as the most exact theoretical
simulation method for continuous-time fOU.

## 5. ARFIMA

ARFIMA means autoregressive fractionally integrated moving average. It extends
ARIMA by allowing the integration parameter to be fractional rather than an
integer.

General form:

```text
phi(B) (1 - B)^d X_t = theta(B) epsilon_t
```

Here:

- `B` is the backshift operator;
- `phi(B)` is the autoregressive part;
- `theta(B)` is the moving-average part;
- `d` is the fractional differencing parameter;
- `epsilon_t` is a white-noise innovation.

The fractional differencing operator is expanded as:

```text
(1 - B)^d =
1 - dB + d(d - 1)B^2 / 2! - d(d - 1)(d - 2)B^3 / 3! + ...
```

In simple long-memory cases:

```text
H = d + 0.5
```

Interpretation:

- `d = 0` gives short memory and `H = 0.5`;
- `0 < d < 0.5` gives stationary long memory and `H > 0.5`;
- negative `d` corresponds to anti-persistence.

ARFIMA is not implemented in the current code because the practical part of the
assignment is focused on fBm/fOU generation and R/S/DFA estimation. It is still
important in the literature review because it is one of the main discrete-time
long-memory models.

Main sources for this part:

- Granger and Joyeux (1980);
- Hosking (1981);
- Beran (1994).
