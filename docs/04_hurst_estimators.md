# Hurst Exponent Estimators

## 1. What the estimators try to measure

The Hurst exponent describes scaling and dependence in a time series. In this
project, the estimators are tested on fractional Gaussian noise generated with a
known true value of `H`.

The main question is:

```text
If the true H is known during simulation, how close is the estimated H?
```

The tested values are:

```text
H = 0.3, 0.5, 0.7, 0.9
```

This range is useful because it includes anti-persistent, neutral, persistent,
and strongly persistent cases.

## 2. R/S analysis

R/S means rescaled range. It is the classical method connected with Hurst's
hydrological work and later with Mandelbrot and Wallis' study of long-run
dependence.

For a window of length `s`, the method works as follows:

1. take a block of data of length `s`;
2. subtract the mean of this block;
3. calculate the cumulative deviations from the mean;
4. compute the range `R` of these cumulative deviations;
5. compute the standard deviation `S` of the original block;
6. calculate `R/S`;
7. repeat for many blocks and many window sizes.

The scaling relation is:

```text
R(s) / S(s) ~ s^H
```

Taking logarithms:

```text
log(R/S) = const + H * log(s)
```

So the slope of the log-log regression is the estimate of `H`.

Code connection:

- function: `estimate_hurst_rs`
- file: `src/estimators.py`
- figure: `04_rs_loglog.png`
- sources: Hurst (1951), Mandelbrot and Wallis (1969)

Strengths:

- simple and historically important;
- easy to implement and explain;
- gives a clear log-log plot.

Weaknesses:

- can be biased in finite samples;
- sensitive to the chosen range of window sizes;
- trends and nonstationarity may distort the estimate.

In the current numerical results, custom R/S preserves the ordering of `H`, but
it is less accurate than custom DFA for several tested values.

## 3. DFA

DFA means detrended fluctuation analysis. It was introduced by Peng et al. and
is widely used for scaling analysis when data may contain trends.

The algorithm:

1. subtract the mean from the series;
2. build the cumulative profile:

```text
Y(k) = sum_{i=1}^{k} (x_i - mean(x))
```

3. split the profile into windows of length `s`;
4. fit a local polynomial trend in each window;
5. subtract the trend;
6. compute the root-mean-square fluctuation `F(s)`;
7. repeat for different scales `s`;
8. estimate the slope of `log F(s)` against `log s`.

The scaling relation is:

```text
F(s) ~ s^H
```

Code connection:

- function: `estimate_hurst_dfa`
- file: `src/estimators.py`
- figure: `05_dfa_loglog.png`
- source: Peng et al. (1994)

Strengths:

- handles local trends better than basic R/S;
- usually stable for scaling analysis;
- produces an interpretable log-log graph.

Weaknesses:

- depends on scale selection;
- polynomial order affects the result;
- very short series can give unstable slopes.

In this project, DFA is the most accurate custom method in the default
experiment.

## 4. Whittle estimator

Whittle estimation is a frequency-domain method. It compares the periodogram of
the observed data with a theoretical spectral density.

The periodogram is a sample estimate of how signal power is distributed across
frequencies. Long-memory processes have important information at low
frequencies, so Whittle-type methods are useful for estimating long-memory
parameters.

A simplified Whittle objective has the form:

```text
sum over frequencies [ I(lambda_j) / f(lambda_j, theta)
                       + log f(lambda_j, theta) ]
```

where:

- `I(lambda_j)` is the periodogram;
- `f(lambda_j, theta)` is the model spectral density;
- `theta` contains the unknown parameters, such as `H` or `d`.

Whittle is not implemented in the first code version because the required
practical part focuses on R/S and DFA. It is reviewed because the assignment
explicitly lists Whittle estimation.

Main sources:

- Beran (1994);
- Dahlhaus (1989);
- Robinson (1995).

## 5. Library estimators

The project also compares the custom code with the `nolds` package:

- `nolds.hurst_rs`;
- `nolds.dfa`.

The purpose is not to replace the custom implementation. The purpose is to have
a reference comparison from a known Python library.

Important implementation detail:

- on this computer, normal `import nolds` may fail because of an internal
  package resource issue;
- the code therefore has a fallback that loads `nolds/measures.py` directly;
- if the package still fails, the experiment writes `NaN` for library methods.

Because `nolds` is slower, the default experiment runs:

```text
custom methods: 100 realizations for each H
nolds methods: 20 realizations for each H
```

The output table includes `estimate_count`, so the reader can see how many
realizations were used for every method.

## 6. Comparison logic

For each true value of `H`, the experiment saves:

- mean estimate;
- standard deviation;
- number of estimates;
- absolute error;
- lag-1 autocorrelation diagnostic.

The main comparison criteria are:

```text
absolute_error = |mean_estimated_H - true_H|
```

The best estimator is not chosen only by one number. It is discussed using:

- accuracy;
- stability;
- visual scaling plots;
- expected ordering of estimates;
- whether the method is understandable for the student project.
