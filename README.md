# Colored Noise and Hurst Exponent Estimation

## Project structure

```text
docs/
  01_problem_statement.md
  02_literature_review.md
  03_models_fbm_fgn_fou_arfima.md
  04_hurst_estimators.md
  05_experiment_design.md
  06_code_sources_and_libraries.md
  07_results_notes.md
src/
  generators.py
  estimators.py
  multifractal.py
  plotting.py
  experiment.py
  main.py
results/
  figures/
  tables/
```

The `docs` folder contains preparation notes for the future final report. The
`src` folder contains the actual code. The `results` folder contains generated
tables and figures.

## How to run

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the full experiment:

```bash
python -m src.main
```

Optional shorter run:

```bash
python -m src.main --n 2048 --repeats 20 --seed 42
```