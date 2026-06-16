# Literature Review

## 1. Colored noise and long memory

Colored noise is a random signal whose power spectrum is not flat. In many
applications it is described by a power law:

```text
S(f) ~ 1 / f^beta
```

White noise has `beta = 0`, pink noise has approximately `beta = 1`, and brown
noise has approximately `beta = 2`. In the context of this project, the most
important colored-noise model is fractional Gaussian noise (`fGn`), because it
has a direct theoretical connection with the Hurst exponent.

For stationary fractional Gaussian noise, the relation between the spectral
exponent and the Hurst exponent is commonly written as:

```text
beta = 2H - 1
```

This means:

- `H < 0.5`: anti-persistent behavior, negative correlation of increments;
- `H = 0.5`: white-noise/Brownian reference case;
- `H > 0.5`: persistent behavior and long-range dependence.

For the code, this section justifies using `fGn` as the main colored-noise
realization with a predefined `H`.

## 2. Hurst exponent and R/S background

The Hurst exponent comes from H. E. Hurst's work on reservoir storage. Hurst
studied long-term dependence in hydrological records and introduced the rescaled
range idea. Later, Mandelbrot and Wallis connected this method with long-run
statistical dependence and fractal behavior.

The R/S statistic studies how the ratio between the range of cumulative
deviations and the standard deviation changes with the window size:

```text
E[R(s) / S(s)] ~ C * s^H
```

Therefore, a log-log regression of `R/S` against the window size `s` gives an
estimate of `H`.

For the code, this literature is used in `src/estimators.py`:

- split the series into windows;
- subtract the local mean;
- calculate cumulative deviations;
- calculate the range `R`;
- divide by the standard deviation `S`;
- estimate the slope on a log-log plot.

Main sources:

- Hurst (1951) for the original long-term storage and rescaled range idea.
- Mandelbrot and Wallis (1969) for the use of R/S in long-run dependence.

## 3. Fractional Brownian motion and fractional Gaussian noise

Fractional Brownian motion (`fBm`) was made widely known by Mandelbrot and Van
Ness. It is a Gaussian self-similar process with stationary increments. The
process is usually denoted by `B_H(t)`, where `H` is the Hurst exponent.

Its covariance function is:

```text
E[B_H(t) B_H(s)] = 0.5 * (|t|^(2H) + |s|^(2H) - |t - s|^(2H))
```

The increment process is fractional Gaussian noise:

```text
X(t) = B_H(t + 1) - B_H(t)
```

This distinction is important for the project:

- `fBm` is non-stationary and useful for sample-path visualization;
- `fGn` is stationary and better suited for estimating `H` by R/S and DFA;
- larger `H` produces smoother fBm paths and more persistent fGn.

For the code, this literature is used in `src/generators.py`:

- generate fBm paths for visual comparison;
- generate fGn as the main colored-noise signal;
- compare behavior for `H = 0.3, 0.5, 0.7, 0.9`.

Main sources:

- Mandelbrot and Van Ness (1968) for the fBm/fGn model.
- Coeurjolly (2000) and Craigmile (2003) for simulation discussion.
- Davies and Harte-type/circulant embedding methods for efficient Gaussian
  long-memory simulation.

## 4. Fractional Ornstein-Uhlenbeck process

The classical Ornstein-Uhlenbeck process is a mean-reverting Gaussian process.
It can be written informally as:

```text
dX_t = -theta * X_t dt + sigma dW_t
```

The fractional Ornstein-Uhlenbeck process replaces the standard Brownian driver
with a fractional Brownian/fractional Gaussian driver:

```text
dX_t = -theta * X_t dt + sigma dB_H(t)
```

This is important because the process keeps mean reversion but also includes
long-memory or roughness controlled by `H`.

For the code, this literature is used in `src/generators.py`:

- generate fOU by an Euler-style discrete recursion;
- use fGn increments as the fractional driving noise;
- show mean-reverting sample paths for different values of `H`.

The implementation is intentionally simple because the assignment requires a
student numerical generator, not a full theoretical fOU simulation package.

Main sources:

- Ornstein-Uhlenbeck process literature for the mean-reverting drift.
- Cheridito, Kawaguchi, and Maejima (2003) for fractional OU processes.
- Comte and Renault (1998) as a continuous-time long-memory modeling reference.

## 5. ARFIMA models

ARFIMA models generalize ARIMA models by allowing the differencing parameter to
be fractional. The model is often written as:

```text
phi(B) (1 - B)^d X_t = theta(B) epsilon_t
```

The fractional differencing operator is expanded as a binomial series:

```text
(1 - B)^d = 1 - dB + d(d - 1)B^2 / 2! - ...
```

For simple long-memory cases, the relation between `d` and the Hurst exponent is:

```text
H = d + 0.5
```

ARFIMA is included because it is a standard discrete-time model for long memory.
It is not implemented in the first version of the code, because the practical
part of the assignment focuses on fBm/fOU generation and R/S/DFA comparison.

Main sources:

- Granger and Joyeux (1980) for long-memory time-series models and fractional
  differencing.
- Hosking (1981) for fractional differencing.
- Beran (1994) for statistical treatment of long-memory processes.

## 6. DFA: detrended fluctuation analysis

DFA was introduced by Peng et al. in the study of DNA sequences. It became a
widely used method for estimating scaling exponents because it can reduce the
effect of local trends.

The main steps are:

1. subtract the mean from the time series;
2. build the cumulative profile;
3. split the profile into windows of size `s`;
4. fit a local polynomial trend inside each window;
5. calculate the root-mean-square fluctuation `F(s)`;
6. estimate the slope of `log F(s)` versus `log s`.

The scaling law is:

```text
F(s) ~ s^H
```

For the code, this source is used in `src/estimators.py`:

- implement DFA manually;
- save the `log F(s)` plot;
- compare DFA accuracy against R/S and optional `nolds` estimates.

Main source:

- Peng et al. (1994) for the DFA method.

## 7. Whittle estimation

Whittle estimation is a frequency-domain method. It uses the periodogram and a
model spectral density. For long-memory processes, the low-frequency behavior of
the spectrum contains information about `H` or the fractional parameter `d`.

In simplified form, the Whittle estimator minimizes an objective based on:

```text
I(lambda) / f(lambda; theta) + log f(lambda; theta)
```

where `I(lambda)` is the periodogram and `f(lambda; theta)` is the theoretical
spectral density.

Whittle estimation is important for the literature review because it is a common
method for long-memory parameter estimation. It is not implemented in the first
code version because R/S and DFA are the required practical estimators in the
assignment.

Main sources:

- Beran (1994) for long-memory statistical models and Whittle estimation.
- Dahlhaus (1989) for efficient parameter estimation in self-similar processes.
- Robinson (1995) for semiparametric frequency-domain estimation.

## 8. Multifractal fluctuation plots

The assignment asks for graphs of multifractal properties. A full multifractal
analysis is larger than the required code, so this project implements a simple
q-order DFA-style fluctuation plot:

```text
F_q(s)
```

Different values of `q` emphasize different fluctuation sizes. Large positive
`q` gives more weight to large fluctuations, while negative `q` gives more
weight to small fluctuations.

For the code, this idea is used in `src/multifractal.py`:

- calculate detrended local variances;
- combine them for several values of `q`;
- plot `F_q(s)` on log-log axes.

This is used as a visual multifractal-style diagnostic, not as a complete
formal multifractal spectrum estimation.

## 9. Source-to-code map

| Topic | Main source | Used in code |
|---|---|---|
| Hurst exponent | Hurst (1951) | interpretation of `H` |
| R/S analysis | Hurst (1951), Mandelbrot and Wallis (1969) | `estimate_hurst_rs` |
| fBm/fGn | Mandelbrot and Van Ness (1968) | `generate_fbm`, `generate_fgn` |
| fGn simulation | Davies-Harte/Craigmile references, `fbm` package | `generate_fgn` |
| fOU | OU literature, Cheridito et al. (2003) | `generate_fou` |
| ARFIMA | Granger and Joyeux (1980), Hosking (1981), Beran (1994) | literature only |
| DFA | Peng et al. (1994) | `estimate_hurst_dfa` |
| Whittle | Beran (1994), Dahlhaus (1989), Robinson (1995) | literature only |
| Library check | `fbm`, `nolds`, `statsmodels` docs | optional comparison and diagnostics |

## References

- Beran, J. (1994). *Statistics for Long-Memory Processes*. Chapman and Hall.
- Cheridito, P., Kawaguchi, H., and Maejima, M. (2003). Fractional Ornstein-Uhlenbeck processes. *Electronic Journal of Probability*, 8, 1-14.
- Coeurjolly, J.-F. (2000). Simulation and identification of the fractional Brownian motion: a bibliographical and comparative study. *Journal of Statistical Software*.
- Comte, F., and Renault, E. (1998). Long memory in continuous-time stochastic volatility models. *Mathematical Finance*, 8(4), 291-323.
- Craigmile, P. F. (2003). Simulating a class of stationary Gaussian processes using the Davies-Harte algorithm. *Journal of Time Series Analysis*, 24(5), 505-511.
- Dahlhaus, R. (1989). Efficient parameter estimation for self-similar processes. *The Annals of Statistics*, 17(4), 1749-1766.
- Granger, C. W. J., and Joyeux, R. (1980). An introduction to long-memory time series models and fractional differencing. *Journal of Time Series Analysis*, 1(1), 15-29.
- Hosking, J. R. M. (1981). Fractional differencing. *Biometrika*, 68(1), 165-176.
- Hurst, H. E. (1951). Long-term storage capacity of reservoirs. *Transactions of the ASCE*, 116, 770-799.
- Mandelbrot, B. B., and Van Ness, J. W. (1968). Fractional Brownian motions, fractional noises and applications. *SIAM Review*, 10(4), 422-437. https://doi.org/10.1137/1010093
- Mandelbrot, B. B., and Wallis, J. R. (1969). Robustness of the rescaled range R/S in the measurement of noncyclic long-run statistical dependence. *Water Resources Research*, 5(5), 967-988. https://doi.org/10.1029/WR005i005p00967
- Peng, C.-K., Buldyrev, S. V., Havlin, S., Simons, M., Stanley, H. E., and Goldberger, A. L. (1994). Mosaic organization of DNA nucleotides. *Physical Review E*, 49, 1685-1689. https://doi.org/10.1103/PhysRevE.49.1685
- Robinson, P. M. (1995). Gaussian semiparametric estimation of long range dependence. *The Annals of Statistics*, 23(5), 1630-1661.
- Taqqu, M. S., Teverovsky, V., and Willinger, W. (1995). Estimators for long-range dependence: an empirical study. *Fractals*, 3(4), 785-798.
