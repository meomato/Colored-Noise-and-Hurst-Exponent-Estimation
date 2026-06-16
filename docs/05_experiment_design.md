# Experiment Design

## 1. Goal

The goal is to generate colored/fractal noise with predefined Hurst exponents
and compare Hurst exponent estimates.

## 2. Tested Hurst values

The default values are:

```text
H = 0.3, 0.5, 0.7, 0.9
```

Reason for each value:

- `H = 0.3`: anti-persistent behavior;
- `H = 0.5`: white-noise/Brownian reference case;
- `H = 0.7`: persistent long-memory behavior;
- `H = 0.9`: strong persistence.

This set is small enough for a student project but wide enough to show the main
change in behavior.

## 3. Default numerical parameters

The default command is:

```bash
python -m src.main
```

Default parameters:

```text
series length: 4096
custom estimator repeats per H: 100
nolds estimator repeats per H: 20
random seed: 42
```

The custom methods are run more times because they are faster and are the main
student implementation. The `nolds` methods are used as a library comparison on
a smaller subset.

Optional command:

```bash
python -m src.main --n 2048 --repeats 20 --library-repeats 5 --seed 42
```

This is useful for a quick test.

## 4. Data generated in the experiment

For every value of `H`, the code generates:

- one sample fGn path for visualization;
- one sample fBm path for visualization;
- one sample fOU path for visualization;
- many fGn realizations for estimator comparison.

The estimator comparison uses fGn because fGn is stationary and directly
connected with the Hurst exponent. fBm is still plotted because it is the most
recognizable fractal process from the literature.

## 5. Estimators compared

The experiment compares:

- `custom_rs`: manual R/S implementation;
- `custom_dfa`: manual DFA implementation;
- `nolds_rs`: library R/S estimate;
- `nolds_dfa`: library DFA estimate.

The custom methods are the main part of the practical work. The library methods
are included to show that the student implementation can be compared with known
tools.

## 6. Metrics saved in the tables

The main summary file is:

```text
results/tables/hurst_estimates.csv
```

It contains:

- `process`: process used for estimation;
- `hurst_true`: true value used during generation;
- `method`: estimation method;
- `estimate_mean`: average estimated value;
- `estimate_std`: standard deviation of estimates;
- `estimate_count`: number of estimates used;
- `lag1_acf_mean`: average lag-1 autocorrelation;
- `absolute_error`: absolute difference between true and estimated `H`.

The raw file is:

```text
results/tables/hurst_estimates_raw.csv
```

It contains one row for each realization and method.

## 7. Figures saved by the code

The code saves these figures:

```text
01_fgn_sample_paths.png
02_fbm_sample_paths.png
03_fou_sample_paths.png
04_rs_loglog.png
05_dfa_loglog.png
06_true_vs_estimated_h.png
07_estimation_error.png
08_multifractal_fluctuations.png
```

Purpose of each figure:

- `01_fgn_sample_paths.png`: shows colored noise for different `H`;
- `02_fbm_sample_paths.png`: shows smoother fBm paths for larger `H`;
- `03_fou_sample_paths.png`: shows mean-reverting fractional paths;
- `04_rs_loglog.png`: shows the R/S scaling relation;
- `05_dfa_loglog.png`: shows the DFA scaling relation;
- `06_true_vs_estimated_h.png`: compares estimates with the ideal line;
- `07_estimation_error.png`: compares estimator errors;
- `08_multifractal_fluctuations.png`: shows q-order fluctuation curves.
