import subprocess

scripts = [

    "src/data_fetch.py",

    "src/fetch_benchmark.py",

    "src/combine_data.py",

    "src/calculations.py",

    "src/sector_analysis.py",

    "src/portfolio_summary.py",

    "src/risk_metrics.py",

    "src/correlation_analysis.py",

    "src/heatmap_visualization.py",

    "src/benchmark_analysis.py",

    "src/excel_export.py"

]

for script in scripts:

    print(f"\nRunning {script}...\n")

    subprocess.run(["python", script])

print("\nFull portfolio analytics pipeline completed.")