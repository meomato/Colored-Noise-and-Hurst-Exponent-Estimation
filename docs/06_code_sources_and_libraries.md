# Code Sources and Libraries

## 1. Short source plan

| Code part | Main source idea | Implementation file |
|---|---|---|
| fBm generation | Mandelbrot and Van Ness model | `src/generators.py` |
| fGn generation | fGn as increments of fBm; Davies-Harte simulation | `src/generators.py` |
| fOU generation | Ornstein-Uhlenbeck mean reversion plus fractional noise driver | `src/generators.py` |
| Power-law colored noise | spectral shaping idea `S(f) ~ 1/f^beta` | `src/generators.py` |
| R/S analysis | Hurst's rescaled range and Mandelbrot-Wallis long-run dependence | `src/estimators.py` |
| DFA | Peng et al. detrended fluctuation analysis | `src/estimators.py` |
| q-order fluctuation plots | DFA-style multifractal fluctuation functions | `src/multifractal.py` |
| Library comparison | `fbm`, `nolds`, `statsmodels` documentation | several files |

## 2. `fbm` package

Used in:

- `src/generators.py`

Imported object:

```python
from fbm import FBM
```

Purpose:

- generate fGn with a predefined Hurst exponent;
- generate fBm with a predefined Hurst exponent;
- use a standard package implementation instead of writing a slow simulator for
  the full experiment.

Code functions:

- `generate_fgn`;
- `generate_fbm`;
- `generate_fbm_from_fgn`.

Literature connection:

- Mandelbrot and Van Ness explain the fBm/fGn model;
- Davies-Harte and Craigmile are connected with efficient simulation of
  stationary Gaussian long-memory processes.

Documentation:

- Python `fbm` package: https://pypi.org/project/fbm/

How it is used in the code:

```python
model = FBM(n=n, hurst=hurst, length=length, method="daviesharte")
values = model.fgn()
```

The package is used for generation, while the main estimators are still written
manually.

## 3. Custom fGn Cholesky generator

Used in:

- `src/generators.py`

Function:

- `generate_fgn_cholesky`

Source idea:

- fGn covariance comes from increments of fBm;
- Gaussian vectors can be generated from a covariance matrix by Cholesky
  decomposition.

Why it is not the main experiment method:

- it is much slower for large `n`;
- the full experiment uses `n = 4096` and many realizations;
- the `fbm` package is more practical for repeated simulation.

## 4. fOU generator

Used in:

- `src/generators.py`

Function:

- `generate_fou`

Source idea:

- classical Ornstein-Uhlenbeck mean reversion;
- fractional OU literature where the driving noise is related to fBm/fGn.

Code idea:

```text
X[t] = X[t-1] - theta * X[t-1] * dt + sigma * dB_H[t]
```

This is a simple Euler-style recursion. It is not claimed to be the most exact
continuous-time simulation method. It is used because it clearly demonstrates
the required idea: mean reversion with fractional colored noise.

Main source:

- Cheridito, Kawaguchi, and Maejima (2003), *Fractional Ornstein-Uhlenbeck processes*.

## 5. Power-law colored noise generator

Used in:

- `src/generators.py`

Function:

- `generate_power_law_noise`

Purpose:

- provide an additional example of colored noise generated through frequency
  shaping;
- connect with the general formula `S(f) ~ 1/f^beta`.

This function is extra. The main experiment uses fGn because its relation with
`H` is clearer.

## 6. Custom R/S implementation

Used in:

- `src/estimators.py`

Function:

- `estimate_hurst_rs`

Source idea:

- Hurst's rescaled range method;
- Mandelbrot and Wallis' use of R/S for long-run dependence.

Code steps:

1. choose several window sizes;
2. split the series into windows;
3. subtract the local mean in every window;
4. compute cumulative deviations;
5. compute the range `R`;
6. compute the standard deviation `S`;
7. average `R/S` for each scale;
8. fit the slope of the log-log relation.

Why it is coded manually:

- R/S is required by the assignment;
- the algorithm is short and explainable;
- the log-log data can be plotted directly.

Output used for figures:

- estimated slope;
- scales;
- average `R/S` values.

## 7. Custom DFA implementation

Used in:

- `src/estimators.py`

Function:

- `estimate_hurst_dfa`

Source idea:

- Peng et al. introduced DFA for scaling analysis.

Code steps:

1. subtract the mean from the series;
2. build the cumulative profile;
3. divide the profile into windows;
4. fit a local polynomial trend;
5. subtract the trend;
6. compute root-mean-square fluctuation;
7. fit the log-log slope.

Why it is coded manually:

- DFA is explicitly required in the assignment;
- it is one of the main methods compared in the experiment;
- the implementation is understandable and defensible.

Output used for figures:

- estimated slope;
- scales;
- fluctuation values `F(s)`.

## 8. `nolds` package

Used in:

- `src/estimators.py`

Purpose:

- optional comparison with library implementations of R/S and DFA.

Functions used when available:

- `hurst_rs`;
- `dfa`.

Important local detail:

- normal `import nolds` may fail on this installation because of an internal
  package resource issue;
- the code therefore tries to load `nolds/measures.py` directly;
- if this also fails, the experiment writes `NaN` for library estimates.

Documentation:

- https://pypi.org/project/nolds/

## 9. `statsmodels`

Used in:

- `src/experiment.py`

Imported as:

```python
import statsmodels.api as sm
```

Purpose:

- calculate lag-1 autocorrelation using `sm.tsa.acf`;
- provide a simple diagnostic confirming persistence or anti-persistence.

Expected diagnostic:

- `H = 0.3`: negative lag-1 autocorrelation;
- `H = 0.5`: autocorrelation close to zero;
- `H = 0.7` and `H = 0.9`: positive autocorrelation.

Documentation:

- https://www.statsmodels.org/

## 10. Multifractal-style fluctuation curves

Used in:

- `src/multifractal.py`

Function:

- `q_order_fluctuations`

Source idea:

- DFA-style fluctuation analysis can be extended to q-order fluctuation
  functions.

Code idea:

1. build the cumulative profile;
2. divide it into windows;
3. detrend each window;
4. compute local variances;
5. combine them for several values of `q`;
6. plot `F_q(s)` against scale.

Values used:

```text
q = -4, -2, 0, 2, 4
```

Interpretation:

- positive `q` emphasizes larger fluctuations;
- negative `q` emphasizes smaller fluctuations;
- different slopes suggest different scaling behavior.

This is included as a visual multifractal-style diagnostic, not a complete
formal multifractal spectrum.

## 11. What is custom and what is library-based

Custom:

- R/S estimator;
- DFA estimator;
- fOU Euler-style generator;
- Cholesky demonstration generator;
- q-order fluctuation curves;
- experiment and plotting logic.

Library-based:

- efficient fGn/fBm generation through `fbm`;
- optional R/S and DFA comparison through `nolds`;
- autocorrelation diagnostic through `statsmodels`.