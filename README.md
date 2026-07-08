# Portfolio Allocation Visualizer

**Turn a spreadsheet of portfolio weights into a clean asset-allocation summary and a stacked-area chart of how the mix shifted over any date range.**

A small pandas + matplotlib toolkit for looking at how a multi-asset portfolio's allocation evolves through time. It rolls granular sub-asset-classes (e.g. *Buyout*, *Venture Capital*) up into their parent classes (*Private Equity*), computes start-vs-end deltas, and renders both a formatted summary table and a stacked-area chart. Comes in two flavors that share the same data:

| File | What it is | Best for |
|------|-----------|----------|
| `allocation_report.py` | Standalone script — generates a start-vs-end summary table (as a styled PNG) and a stacked-area chart for a fixed date range | Producing a shareable report / image |
| `dashboard_streamlit.py` | Interactive Streamlit app — pick the start/end month-year from a sidebar and see the chart update live | Exploring the data interactively |

---

## What it does

- **Sub-class → main-class rollup.** Granular holdings are aggregated into their parent asset classes (Public Equity, Hedge Funds, Private Equity, Real Assets, Fixed Income, Cash) via an explicit mapping, so the chart stays readable while the table can still drill into sub-classes.
- **Start-vs-end delta table.** For any two dates, it builds a table of each class's weight at the start, at the end, and the change between — bold parent rows, indented sub-rows — and saves it as a clean image (`allocation_report.py`).
- **Nearest-prior month-end matching.** Ask for *Dec 2022* and it snaps to the closest available month-end at or before that date, so you never crash on a month the data doesn't have.
- **Stacked-area chart** of allocation over the selected window, with percent-formatted axes and start/end markers.

---

## Input format

Both scripts read a single Excel file, `weights.xlsx`, with:

- a **`Date`** column (month-end dates), and
- one column per asset class and sub-asset-class, holding that period's weight as a decimal (e.g. `0.24` for 24%).

A sample `weights.xlsx` is included so you can run either script immediately.

> Note on the convention: weights above 100% represent a negative cash allocation (leverage), rendered as-is so the stacked areas still sum correctly.

---

## Run it

```bash
pip install -r requirements.txt
```

**Report script** — edit the date range at the top of the file, then:

```bash
python allocation_report.py
# writes asset_allocation_summary.png and shows the stacked-area chart
```

**Interactive dashboard:**

```bash
streamlit run dashboard_streamlit.py
# opens in your browser; choose the date range from the sidebar
```

---

## Tech

pandas (datetime indexing, sub-class aggregation, nearest-prior-date lookup) · matplotlib (`stackplot`, styled table rendering, percent formatting) · openpyxl (Excel ingestion) · Streamlit (interactive dashboard).
