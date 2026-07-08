import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ---- User input ----
user_start_year, user_start_month = 2022, 12
user_end_year, user_end_month = 2025, 3

excel_cols = [
    "Public Equity", "U.S.", "Non-U.S.",
    "Hedge Funds", "Long / Short", "Opportunistic Hedge Funds",
    "Private Equity", "Buyout", "Venture Capital", "Private Alternatives",
    "Real Assets", "Real Estate", "Natural Resources",
    "Fixed Income", "Cash"
]

asset_classes = [
    "Public Equity", "Hedge Funds", "Private Equity",
    "Real Assets", "Fixed Income", "Cash"
]

sub_to_main = {
    "U.S.": "Public Equity",
    "Non-U.S.": "Public Equity",
    "Long / Short": "Hedge Funds",
    "Opportunistic Hedge Funds": "Hedge Funds",
    "Buyout": "Private Equity",
    "Venture Capital": "Private Equity",
    "Private Alternatives": "Private Equity",
    "Real Estate": "Real Assets",
    "Natural Resources": "Real Assets"
}
for cls in asset_classes:
    sub_to_main[cls] = cls

df = pd.read_excel('weights.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# ---- Helper: Nearest previous available end-of-month ----
def get_month_end_or_prev(year, month, index):
    candidates = [dt for dt in index if (dt.year < year) or (dt.year == year and dt.month <= month)]
    matches = [dt for dt in candidates if dt.year == year and dt.month == month]
    return max(matches) if matches else max(candidates)

start_date = get_month_end_or_prev(user_start_year, user_start_month, df.index)
end_date   = get_month_end_or_prev(user_end_year, user_end_month, df.index)

row_start = df.loc[start_date]
row_end   = df.loc[end_date]

print(f"Using start date: {start_date.strftime('%Y-%m-%d')}")
print(f"Using end date:   {end_date.strftime('%Y-%m-%d')}")

# ---- Display summary table for asset classes and sub-classes ----
rows = []
indent = "  "
for main_cls in asset_classes:
    val_start = row_start.get(main_cls, None)
    val_end   = row_end.get(main_cls, None)
    delta     = (val_end - val_start) if (val_start is not None and val_end is not None) else None
    rows.append([
        main_cls, 
        f"{val_start*100:.1f}%" if val_start is not None else "-", 
        f"{val_end*100:.1f}%" if val_end is not None else "-", 
        f"{delta*100:+.1f}%" if delta is not None else "-"
    ])
    subclass_cols = [c for c in df.columns if sub_to_main.get(c) == main_cls and c != main_cls]
    for subc in subclass_cols:
        sub_start = row_start.get(subc, None)
        sub_end   = row_end.get(subc, None)
        delta_sub = (sub_end - sub_start) if (sub_start is not None and sub_end is not None) else None
        rows.append([
            f"{indent}{subc}", 
            f"{sub_start*100:.1f}%" if sub_start is not None else "-", 
            f"{sub_end*100:.1f}%" if sub_end is not None else "-", 
            f"{delta_sub*100:+.1f}%" if delta_sub is not None else "-"
        ])

summary_df = pd.DataFrame(rows, columns=["Asset Class", f"{start_date.strftime('%b-%Y')}", f"{end_date.strftime('%b-%Y')}", "Delta"])
print(summary_df.to_string(index=False))

# ---- Table as nicely formatted image ----
table_data = summary_df.values.tolist()
column_labels = summary_df.columns.tolist()

fig, ax = plt.subplots(figsize=(7, len(table_data)*0.45+1.8))  # Dynamic height
ax.axis('off')

the_table = ax.table(
    cellText=table_data,
    colLabels=column_labels,
    cellLoc='right',
    loc='center'
)

# Styling: bold main class, normal indented subclass, nice headers
for i, row in enumerate(table_data):
    asset_class = row[0]
    cell = the_table[i + 1, 0]  # +1 for header
    if not asset_class.startswith("  "):
        cell.set_text_props(weight='bold', fontsize=13)
        cell.set_facecolor('#E3EBF7')
    else:
        cell.set_text_props(fontsize=11, color='#222222')

# Make the leftmost column (column 0) about 1.5x wider
col_widths = [0.40, 0.18, 0.18, 0.18]  # Adjust as needed; first value larger

for i in range(len(table_data) + 1):  # +1 for header row
    for j, width in enumerate(col_widths):
        the_table[i, j].set_width(width)

# Header formatting (your provided code, adjusted location)
for j in range(len(column_labels)):
    the_table[0, j].set_text_props(weight='bold', fontsize=13, color='#1a3c5d')
    the_table[0, j].set_facecolor('#bfcde0')

the_table.auto_set_font_size(False)
the_table.set_fontsize(12)
the_table.scale(1.1, 1.3)

plt.tight_layout()
plt.savefig('asset_allocation_summary.png', bbox_inches='tight', dpi=240)
plt.close()

print("Summary table image saved as asset_allocation_summary.png")

# ---- Stacked Area Chart for asset classes (restricted to date range) ----
plot_df = pd.DataFrame(index=df.index)
for main_cls in asset_classes:
    subclass_cols = [c for c in df.columns if sub_to_main.get(c) == main_cls and c != main_cls]
    if subclass_cols:
        plot_df[main_cls] = df[subclass_cols].sum(axis=1)
    else:
        plot_df[main_cls] = df[main_cls]

mask = (plot_df.index >= start_date) & (plot_df.index <= end_date)
plot_df_range = plot_df.loc[mask]

fig, ax = plt.subplots(figsize=(12, 6))
ax.stackplot(plot_df_range.index, *(plot_df_range[cls] * 100 for cls in asset_classes),
             labels=asset_classes, alpha=0.8)
ax.axhline(0, color='black', linewidth=1, linestyle='--')
ax.set_ylabel("Weight (%)")
ax.set_xlabel("Date")
ax.set_title(f"Asset Class Weights {start_date.strftime('%b-%Y')} to {end_date.strftime('%b-%Y')}")
ax.legend(loc='upper right')
ax.yaxis.set_major_formatter(PercentFormatter())

# Annotate start/end dates
for xd in [start_date, end_date]:
    ax.axvline(x=xd, color='red', linestyle=':', linewidth=1)

plt.tight_layout()
plt.show()
