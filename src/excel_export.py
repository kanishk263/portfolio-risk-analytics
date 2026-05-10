"""Build a polished Excel dashboard from pipeline export CSV files."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXPORTS_DIR = ROOT / "data" / "exports"
DASHBOARD_DIR = ROOT / "dashboard"
OUTPUT_FILE = DASHBOARD_DIR / "Portfolio_Analytics_Dashboard.xlsx"


FILES = {
    "portfolio_summary": EXPORTS_DIR / "portfolio_summary.csv",
    "portfolio_level": EXPORTS_DIR / "portfolio_level_summary.csv",
    "sector_allocation": EXPORTS_DIR / "sector_allocation.csv",
    "risk_metrics": EXPORTS_DIR / "risk_metrics.csv",
    "benchmark_comparison": EXPORTS_DIR / "benchmark_comparison.csv",
    "correlation_matrix": EXPORTS_DIR / "correlation_matrix.csv",
}


COLORS = {
    "ink": "#17212B",
    "slate": "#2F3A45",
    "panel": "#EEF3F7",
    "line": "#D7DEE5",
    "blue": "#2563EB",
    "teal": "#0F766E",
    "green": "#16A34A",
    "red": "#DC2626",
    "amber": "#D97706",
    "white": "#FFFFFF",
    "muted": "#64748B",
}


def load_exports() -> dict[str, pd.DataFrame]:
    missing = [str(path) for path in FILES.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing export files. Run the pipeline before creating the dashboard:\n"
            + "\n".join(missing)
        )

    return {
        "portfolio_summary": pd.read_csv(FILES["portfolio_summary"]),
        "portfolio_level": pd.read_csv(FILES["portfolio_level"]),
        "sector_allocation": pd.read_csv(FILES["sector_allocation"]),
        "risk_metrics": pd.read_csv(FILES["risk_metrics"]),
        "benchmark_comparison": pd.read_csv(FILES["benchmark_comparison"]),
        "correlation_matrix": pd.read_csv(FILES["correlation_matrix"], index_col=0),
    }


def add_title(worksheet, workbook, title: str, subtitle: str) -> None:
    title_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 22,
            "font_color": COLORS["white"],
            "bg_color": COLORS["ink"],
            "valign": "vcenter",
        }
    )
    subtitle_format = workbook.add_format(
        {
            "font_size": 11,
            "font_color": "#D7DEE5",
            "bg_color": COLORS["slate"],
            "valign": "vcenter",
        }
    )
    worksheet.merge_range("A1:L1", title, title_format)
    worksheet.merge_range("A2:L2", subtitle, subtitle_format)
    worksheet.set_row(0, 34)
    worksheet.set_row(1, 26)


def add_section(worksheet, workbook, cell_range: str, label: str) -> None:
    section_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "font_color": COLORS["ink"],
            "bg_color": COLORS["panel"],
            "border": 1,
            "border_color": COLORS["line"],
        }
    )
    worksheet.merge_range(cell_range, label, section_format)


def add_kpi_card(
    worksheet,
    workbook,
    cell_range: str,
    label: str,
    value,
    value_format: str,
    color: str,
) -> None:
    label_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 10,
            "font_color": COLORS["muted"],
            "bg_color": COLORS["white"],
            "border": 1,
            "border_color": COLORS["line"],
            "valign": "vcenter",
        }
    )
    value_fmt = workbook.add_format(
        {
            "bold": True,
            "font_size": 18,
            "font_color": color,
            "bg_color": COLORS["white"],
            "border": 1,
            "border_color": COLORS["line"],
            "num_format": value_format,
            "valign": "vcenter",
        }
    )
    note_format = workbook.add_format(
        {
            "font_size": 8,
            "font_color": COLORS["muted"],
            "bg_color": COLORS["white"],
            "border": 1,
            "border_color": COLORS["line"],
            "valign": "vcenter",
        }
    )
    start, end = cell_range.split(":")
    start_col = ord(start[0]) - 65
    end_col = ord(end[0]) - 65
    start_row = int(start[1:]) - 1

    worksheet.merge_range(start_row, start_col, start_row, end_col, label, label_format)
    worksheet.merge_range(
        start_row + 1,
        start_col,
        start_row + 1,
        end_col,
        value,
        value_fmt,
    )
    worksheet.merge_range(
        start_row + 2,
        start_col,
        start_row + 2,
        end_col,
        "Auto refreshed from pipeline exports",
        note_format,
    )


def add_dataframe(
    worksheet,
    workbook,
    df: pd.DataFrame,
    start_row: int,
    start_col: int,
    money_cols: list[str] | None = None,
    percent_cols: list[str] | None = None,
) -> None:
    money_cols = money_cols or []
    percent_cols = percent_cols or []
    header_format = workbook.add_format(
        {
            "bold": True,
            "font_color": COLORS["white"],
            "bg_color": COLORS["ink"],
            "border": 1,
            "border_color": COLORS["ink"],
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True,
        }
    )
    text_format = workbook.add_format(
        {"border": 1, "border_color": COLORS["line"], "valign": "vcenter"}
    )
    money_format = workbook.add_format(
        {
            "num_format": "#,##0.00",
            "border": 1,
            "border_color": COLORS["line"],
            "valign": "vcenter",
        }
    )
    percent_format = workbook.add_format(
        {
            "num_format": "0.00",
            "border": 1,
            "border_color": COLORS["line"],
            "valign": "vcenter",
        }
    )

    for idx, column in enumerate(df.columns):
        worksheet.write(start_row, start_col + idx, column, header_format)

    for row_idx, row in df.reset_index(drop=True).iterrows():
        for col_idx, column in enumerate(df.columns):
            fmt = text_format
            if column in money_cols:
                fmt = money_format
            elif column in percent_cols:
                fmt = percent_format
            value = row[column]
            if pd.isna(value):
                value = ""
            worksheet.write(start_row + row_idx + 1, start_col + col_idx, value, fmt)


def add_insights(worksheet, workbook, data: dict[str, pd.DataFrame]) -> None:
    portfolio_level = data["portfolio_level"]
    portfolio_summary = data["portfolio_summary"]
    sector_allocation = data["sector_allocation"]
    risk_metrics = data["risk_metrics"]

    worst_portfolio = portfolio_level.sort_values("Portfolio Return %").iloc[0]
    best_holding = portfolio_summary.sort_values("Absolute Return %", ascending=False).iloc[0]
    worst_holding = portfolio_summary.sort_values("Absolute Return %").iloc[0]
    largest_sector = sector_allocation.sort_values("Allocation %", ascending=False).iloc[0]
    highest_vol = risk_metrics.sort_values("Volatility", ascending=False).iloc[0]

    rows = [
        [
            "Performance",
            f"{worst_portfolio['Portfolio']} is the weakest portfolio at "
            f"{worst_portfolio['Portfolio Return %']:.2f}% return.",
            "Review drawdown drivers and benchmark fit.",
        ],
        [
            "Holding Quality",
            f"{best_holding['Ticker']} is the best performer at "
            f"{best_holding['Absolute Return %']:.2f}%; {worst_holding['Ticker']} "
            f"is weakest at {worst_holding['Absolute Return %']:.2f}%.",
            "Separate structural winners from short-term price moves.",
        ],
        [
            "Concentration",
            f"{largest_sector['Sector']} has the largest sector weight at "
            f"{largest_sector['Allocation %']:.2f}%.",
            "Set target allocation bands and rebalance if needed.",
        ],
        [
            "Risk",
            f"{highest_vol['Ticker']} has the highest annualized volatility at "
            f"{highest_vol['Volatility']:.2f}%.",
            "Check whether risk contribution is justified by return.",
        ],
    ]

    header_format = workbook.add_format(
        {
            "bold": True,
            "font_color": COLORS["white"],
            "bg_color": COLORS["ink"],
            "border": 1,
            "border_color": COLORS["line"],
        }
    )
    body_format = workbook.add_format(
        {
            "text_wrap": True,
            "valign": "top",
            "border": 1,
            "border_color": COLORS["line"],
        }
    )
    worksheet.write_row("A43", ["Theme", "Insight", "Action"], header_format)
    for row_number, row in enumerate(rows, start=44):
        worksheet.write(row_number - 1, 0, row[0], body_format)
        worksheet.write(row_number - 1, 1, row[1], body_format)
        worksheet.write(row_number - 1, 2, row[2], body_format)
        worksheet.set_row(row_number - 1, 42)


def build_dashboard(data: dict[str, pd.DataFrame]) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        workbook = writer.book
        workbook.set_properties(
            {
                "title": "Family Investment Intelligence Dashboard",
                "subject": "Portfolio risk analytics",
                "author": "Portfolio Risk Analytics Pipeline",
            }
        )

        sheets = {
            "Executive Dashboard": workbook.add_worksheet("Executive Dashboard"),
            "Portfolio Analytics": workbook.add_worksheet("Portfolio Analytics"),
            "Risk Analytics": workbook.add_worksheet("Risk Analytics"),
            "Allocation & Benchmark": workbook.add_worksheet("Allocation & Benchmark"),
        }

        for sheet in sheets.values():
            sheet.hide_gridlines(2)
            sheet.set_default_row(21)
            sheet.set_column("A:L", 14)

        raw_sheets = {
            "Stock Analytics": data["portfolio_summary"],
            "Portfolio Summary": data["portfolio_level"],
            "Sector Allocation": data["sector_allocation"],
            "Risk Metrics": data["risk_metrics"],
            "Benchmark Comparison": data["benchmark_comparison"],
            "Correlation Matrix": data["correlation_matrix"].reset_index(),
        }
        for sheet_name, df in raw_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes(1, 0)
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
            worksheet.set_column(0, len(df.columns) - 1, 16)

        dashboard = sheets["Executive Dashboard"]
        add_title(
            dashboard,
            workbook,
            "Family Investment Intelligence Dashboard",
            "Executive snapshot of portfolio value, return, allocation, risk, and benchmark performance",
        )
        total_invested = data["portfolio_level"]["Invested Amount"].sum()
        current_value = data["portfolio_level"]["Current Value"].sum()
        profit_loss = data["portfolio_level"]["Profit/Loss"].sum()
        family_return = profit_loss / total_invested if total_invested else 0
        benchmark_return = data["benchmark_comparison"]["Benchmark Return %"].mean() / 100

        add_kpi_card(dashboard, workbook, "A4:B6", "Total Invested", total_invested, "#,##0", COLORS["blue"])
        add_kpi_card(dashboard, workbook, "C4:D6", "Current Value", current_value, "#,##0", COLORS["teal"])
        add_kpi_card(dashboard, workbook, "E4:F6", "Unrealized P/L", profit_loss, "#,##0", COLORS["red"])
        add_kpi_card(dashboard, workbook, "G4:H6", "Family Return", family_return, "0.00%", COLORS["red"])
        add_kpi_card(dashboard, workbook, "I4:J6", "Benchmark Return", benchmark_return, "0.00%", COLORS["amber"])
        add_kpi_card(
            dashboard,
            workbook,
            "K4:L6",
            "Relative Return",
            family_return - benchmark_return,
            "0.00%",
            COLORS["red"],
        )

        add_section(dashboard, workbook, "A8:F8", "Portfolio Value by Strategy")
        add_section(dashboard, workbook, "G8:L8", "Portfolio Return vs Benchmark")
        add_section(dashboard, workbook, "A25:F25", "Sector Allocation")
        add_section(dashboard, workbook, "G25:L25", "Risk-Adjusted Return Quality")
        add_section(dashboard, workbook, "A42:L42", "Automated Investment Insights")
        add_insights(dashboard, workbook, data)
        dashboard.set_column("A:A", 18)
        dashboard.set_column("B:B", 78)
        dashboard.set_column("C:C", 56)

        chart1 = workbook.add_chart({"type": "column"})
        chart1.add_series(
            {
                "name": "Invested",
                "categories": "='Portfolio Summary'!$A$2:$A$4",
                "values": "='Portfolio Summary'!$B$2:$B$4",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart1.add_series(
            {
                "name": "Current",
                "categories": "='Portfolio Summary'!$A$2:$A$4",
                "values": "='Portfolio Summary'!$C$2:$C$4",
                "fill": {"color": "#F97316"},
            }
        )
        chart1.set_title({"name": "Invested Amount vs Current Value"})
        chart1.set_legend({"position": "bottom"})
        dashboard.insert_chart("A9", chart1, {"x_scale": 1.58, "y_scale": 1.22})

        chart2 = workbook.add_chart({"type": "column"})
        chart2.add_series(
            {
                "name": "Portfolio Return %",
                "categories": "='Benchmark Comparison'!$A$2:$A$4",
                "values": "='Benchmark Comparison'!$E$2:$E$4",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart2.add_series(
            {
                "name": "Benchmark Return %",
                "categories": "='Benchmark Comparison'!$A$2:$A$4",
                "values": "='Benchmark Comparison'!$F$2:$F$4",
                "fill": {"color": "#F97316"},
            }
        )
        chart2.set_title({"name": "Return % vs Benchmark %"})
        chart2.set_legend({"position": "bottom"})
        dashboard.insert_chart("G9", chart2, {"x_scale": 1.58, "y_scale": 1.22})

        chart3 = workbook.add_chart({"type": "doughnut"})
        chart3.add_series(
            {
                "name": "Allocation %",
                "categories": "='Sector Allocation'!$A$2:$A$5",
                "values": "='Sector Allocation'!$C$2:$C$5",
            }
        )
        chart3.set_title({"name": "Current Value Allocation %"})
        chart3.set_legend({"position": "right"})
        dashboard.insert_chart("A26", chart3, {"x_scale": 1.58, "y_scale": 1.14})

        chart4 = workbook.add_chart({"type": "bar"})
        chart4.add_series(
            {
                "name": "Sharpe Ratio",
                "categories": "='Risk Metrics'!$A$2:$A$7",
                "values": "='Risk Metrics'!$D$2:$D$7",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart4.set_title({"name": "Sharpe Ratio by Holding"})
        chart4.set_legend({"none": True})
        dashboard.insert_chart("G26", chart4, {"x_scale": 1.58, "y_scale": 1.14})

        portfolio_sheet = sheets["Portfolio Analytics"]
        add_title(
            portfolio_sheet,
            workbook,
            "Portfolio Analytics",
            "Strategy-level and holding-level performance review",
        )
        chart5 = workbook.add_chart({"type": "column"})
        chart5.add_series(
            {
                "name": "Current Value",
                "categories": "='Stock Analytics'!$C$2:$C$7",
                "values": "='Stock Analytics'!$J$2:$J$7",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart5.set_title({"name": "Holding Current Value"})
        chart5.set_legend({"none": True})
        portfolio_sheet.insert_chart("A4", chart5, {"x_scale": 1.58, "y_scale": 1.15})

        chart6 = workbook.add_chart({"type": "column"})
        chart6.add_series(
            {
                "name": "Absolute Return %",
                "categories": "='Stock Analytics'!$C$2:$C$7",
                "values": "='Stock Analytics'!$L$2:$L$7",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart6.set_title({"name": "Holding Absolute Return %"})
        chart6.set_legend({"none": True})
        portfolio_sheet.insert_chart("G4", chart6, {"x_scale": 1.58, "y_scale": 1.15})
        add_section(portfolio_sheet, workbook, "A19:E19", "Portfolio-Level Summary")
        add_dataframe(
            portfolio_sheet,
            workbook,
            data["portfolio_level"],
            19,
            0,
            money_cols=["Invested Amount", "Current Value", "Profit/Loss"],
            percent_cols=["Portfolio Return %"],
        )
        add_section(portfolio_sheet, workbook, "A25:L25", "Holding-Level Analytics")
        add_dataframe(
            portfolio_sheet,
            workbook,
            data["portfolio_summary"],
            25,
            0,
            money_cols=["Buy Price", "Current Price", "Invested Amount", "Current Value", "Profit/Loss"],
            percent_cols=["Absolute Return %", "CAGR %"],
        )
        portfolio_sheet.set_column("A:A", 16)
        portfolio_sheet.set_column("B:D", 15)
        portfolio_sheet.set_column("E:L", 14)

        risk_sheet = sheets["Risk Analytics"]
        add_title(
            risk_sheet,
            workbook,
            "Risk Analytics",
            "Return, volatility, Sharpe ratio, drawdown, and correlation heatmap",
        )
        add_dataframe(
            risk_sheet,
            workbook,
            data["risk_metrics"],
            3,
            0,
            percent_cols=["Annual Return", "Volatility", "Sharpe Ratio", "Maximum Drawdown"],
        )
        add_dataframe(
            risk_sheet,
            workbook,
            data["correlation_matrix"].reset_index(),
            3,
            6,
            percent_cols=list(data["correlation_matrix"].columns),
        )
        chart7 = workbook.add_chart({"type": "column"})
        chart7.add_series(
            {
                "name": "Annual Return %",
                "categories": "='Risk Metrics'!$A$2:$A$7",
                "values": "='Risk Metrics'!$B$2:$B$7",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart7.add_series(
            {
                "name": "Volatility %",
                "categories": "='Risk Metrics'!$A$2:$A$7",
                "values": "='Risk Metrics'!$C$2:$C$7",
                "fill": {"color": "#F97316"},
            }
        )
        chart7.set_title({"name": "Annual Return vs Volatility"})
        chart7.set_legend({"position": "bottom"})
        risk_sheet.insert_chart("A15", chart7, {"x_scale": 2.42, "y_scale": 1.35})

        allocation_sheet = sheets["Allocation & Benchmark"]
        add_title(
            allocation_sheet,
            workbook,
            "Allocation & Benchmark",
            "Sector exposure, allocation concentration, and relative performance",
        )
        chart8 = workbook.add_chart({"type": "doughnut"})
        chart8.add_series(
            {
                "name": "Allocation %",
                "categories": "='Sector Allocation'!$A$2:$A$5",
                "values": "='Sector Allocation'!$C$2:$C$5",
            }
        )
        chart8.set_title({"name": "Sector Allocation %"})
        chart8.set_legend({"position": "right"})
        allocation_sheet.insert_chart("A4", chart8, {"x_scale": 1.58, "y_scale": 1.22})

        chart9 = workbook.add_chart({"type": "column"})
        chart9.add_series(
            {
                "name": "Outperformance",
                "categories": "='Benchmark Comparison'!$A$2:$A$4",
                "values": "='Benchmark Comparison'!$G$2:$G$4",
                "fill": {"color": COLORS["teal"]},
            }
        )
        chart9.set_title({"name": "Portfolio Outperformance"})
        chart9.set_legend({"none": True})
        allocation_sheet.insert_chart("G4", chart9, {"x_scale": 1.58, "y_scale": 1.22})
        add_section(allocation_sheet, workbook, "A20:C20", "Sector Allocation Table")
        add_dataframe(
            allocation_sheet,
            workbook,
            data["sector_allocation"],
            20,
            0,
            money_cols=["Current Value"],
            percent_cols=["Allocation %"],
        )
        add_section(allocation_sheet, workbook, "E20:K20", "Benchmark Comparison Table")
        add_dataframe(
            allocation_sheet,
            workbook,
            data["benchmark_comparison"],
            20,
            4,
            money_cols=["Invested Amount", "Current Value", "Profit/Loss"],
            percent_cols=["Portfolio Return %", "Benchmark Return %", "Outperformance"],
        )
        allocation_sheet.set_column("A:L", 15)

    print(f"\nExcel dashboard exported successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_dashboard(load_exports())
