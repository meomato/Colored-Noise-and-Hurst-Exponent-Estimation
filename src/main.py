"""Command line entry point for the project."""

from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import ExperimentConfig, run_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Colored noise and Hurst exponent experiment")
    parser.add_argument("--n", type=int, default=4096, help="length of each generated series")
    parser.add_argument("--repeats", type=int, default=100, help="number of realizations for each H")
    parser.add_argument("--library-repeats", type=int, default=20, help="realizations per H for slower library estimates")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ExperimentConfig(n=args.n, repeats=args.repeats, library_repeats=args.library_repeats, seed=args.seed)
    base_dir = Path(__file__).resolve().parents[1]
    summary = run_experiment(config, base_dir)
    print("Experiment finished.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
