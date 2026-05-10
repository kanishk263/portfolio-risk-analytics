"""Run the full portfolio analytics pipeline.

The scripts are intentionally kept modular so each analytics step can also be
run independently during development.
"""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    "src/data_fetch.py",
    "src/fetch_benchmark.py",
    "src/combine_data.py",
    "src/calculations.py",
    "src/sector_analysis.py",
    "src/visualization.py",
    "src/portfolio_summary.py",
    "src/risk_metrics.py",
    "src/correlation_analysis.py",
    "src/heatmap_visualization.py",
    "src/benchmark_analysis.py",
    "src/excel_export.py",
]


def run_pipeline() -> None:
    for script in PIPELINE_STEPS:
        print(f"\nRunning {script}...\n")
        subprocess.run(
            [sys.executable, str(ROOT / script)],
            cwd=ROOT,
            check=True,
        )


if __name__ == "__main__":
    run_pipeline()
    print("\nFull portfolio analytics pipeline completed.")
