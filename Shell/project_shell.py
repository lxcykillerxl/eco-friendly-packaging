import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import textwrap

# ------------------------------
# Config & Data
# ------------------------------
st.set_page_config(page_title="Eco-Friendly Packaging", layout="wide")

# Load dataset (place eco_friendly_multi.csv in same directory)
df = pd.read_csv("eco_friendly.csv")

# ------------------------------
# Helpers
# ------------------------------
def shorten_label(s: str, max_len: int = 14) -> str:
    """Shorten long labels for axis ticks while keeping readability."""
    if s is None:
        return ""
    s = str(s)
    if len(s) <= max_len:
        return s
    return textwrap.shorten(s, width=max_len, placeholder="...")

def convert_to_years(val):
    """Convert strings ('2 years','6 months','30 days','Reusable') to numeric years. Reusable -> 0.0"""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    v = str(val).strip().lower()
    if v == "reusable":
        return 0.0
    parts = v.split()
    try:
        num = float(parts[0])
    except:
        return None
    if "year" in v:
        return num
    if "month" in v:
        return num / 12.0
    if "day" in v:
        return num / 365.0
    return None

# ------------------------------
# Styling (cards)
# ------------------------------
st.markdown(
    """
<style>
    .eco-card {
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 10px;
        background-color: #d1fae5; /* soft green */
        border: 1px solid #10b981;
        color: #064e3b; /* dark green text */
        font-weight: 500;
    }
    .old-card {
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 10px;
        background-color: #fee2e2; /* soft red */
        border: 1px solid #ef4444;
        color: #7f1d1d; /* dark red text */
        font-weight: 500;
    }
    .summary-card {
        padding: 12px;
        border-radius: 10px;
        background-color: #bfdbfe; /* soft blue */
        border: 1px solid #3b82f6;
        color: #1e3a8a; /* dark blue text */
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------
# UI: Title & input
# ------------------------------
st.title("🌍 Eco-Friendly Packaging Comparison Tool")
st.caption("Enter a product name exactly as in the CSV (case-insensitive). Examples: Banana, Milk, Apple")

product_input = st.text_input("🔍 Enter product name:", "").strip()

if not product_input:
    st.info("Type a product name above to view packaging details and comparisons.")
    st.stop()

# ------------------------------
# Lookup product row
# ------------------------------
matches = df[df["Product_Name"].str.lower() == product_input.lower()]

if matches.empty:
    st.error("❌ Product not found. Check spelling or try another product name.")
    sample_names = ", ".join(list(df["Product_Name"].unique()[:12]))
    st.write("Try one of these sample product names:", sample_names)
    st.stop()

row = matches.iloc[0]

# ------------------------------
# Layout: left details (wider) | right charts (vertical)
# ------------------------------
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("❌ Old Packaging")
    st.markdown(
        f"""
        <div class="old-card">
        <b>Packaging:</b> {row.get('Old_Packaging', 'N/A')}<br>
        <b>CO₂ Score:</b> {row.get('Old_CO2', 'N/A')} kg CO₂/kg<br>
        <b>Shelf Life:</b> {row.get('Old_Shelf_Life', 'N/A')}<br>
        <b>Decomposition:</b> {row.get('Old_Decomposition', 'N/A')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("✅ Eco-Friendly Alternatives")
    found_any = False
    for i in range(1, 4):
        name_key = f"New_Packaging_{i}"
        if pd.notna(row.get(name_key)):
            found_any = True
            with st.expander(f"Option {i}: {row[name_key]}"):
                st.markdown(
                    f"""
                    <div class="eco-card">
                    🌱 <b>CO₂:</b> {row.get(f'New_CO2_{i}', 'N/A')} kg CO₂/kg<br>
                    ⏳ <b>Shelf Life:</b> {row.get(f'New_Shelf_Life_{i}', 'N/A')}<br>
                    ♻️ <b>Decomposition:</b> {row.get(f'New_Decomposition_{i}', 'N/A')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    if not found_any:
        st.write("No eco-friendly alternatives available for this product in the dataset.")

with col_right:
    st.subheader("📊 Comparison Charts")

    # Build label lists and numeric values
    labels_full = ["Old"]
    co2_vals = []
    decomp_vals = []

    # Old values
    try:
        co2_old = float(row.get("Old_CO2")) if pd.notna(row.get("Old_CO2")) else np.nan
    except:
        co2_old = np.nan
    labels_full = ["Old"]
    co2_vals = [co2_old]
    decomp_vals = [convert_to_years(row.get("Old_Decomposition"))]

    # New options
    for i in range(1, 4):
        pkg_key = f"New_Packaging_{i}"
        co2_key = f"New_CO2_{i}"
        decomp_key = f"New_Decomposition_{i}"
        if pd.notna(row.get(pkg_key)):
            labels_full.append(row.get(pkg_key))
            # CO2
            try:
                co2_val = float(row.get(co2_key)) if pd.notna(row.get(co2_key)) else np.nan
            except:
                co2_val = np.nan
            co2_vals.append(co2_val)
            # Decomp
            decomp_vals.append(convert_to_years(row.get(decomp_key)))

    # Shorten labels for plotting so they fit
    labels_short = [shorten_label(s, max_len=14) for s in labels_full]

    # Colors
    co2_colors = ["#ef4444"] + ["#059669"] * (len(co2_vals) - 1)
    decomp_colors = ["#ef4444"] + ["#7c3aed"] * (len(decomp_vals) - 1)

    # ------- Chart 1: CO2 (full width of right column) -------
    fig, ax = plt.subplots(figsize=(6, 3.2))
    x = np.arange(len(labels_short))
    co2_plot_values = [float(v) if (v is not None and not (isinstance(v, float) and np.isnan(v))) else 0.0 for v in co2_vals]
    ax.bar(x, co2_plot_values, color=co2_colors)
    ax.set_title("CO₂ Comparison", fontsize=12, fontweight="bold")
    ax.set_ylabel("kg CO₂ / kg", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels_short, rotation=30, ha="right", fontsize=9)
    ax.tick_params(axis="y", labelsize=9)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # ------- Chart 2: Decomposition (stacked below CO2) -------
    fig2, ax2 = plt.subplots(figsize=(6, 3.2))
    x2 = np.arange(len(labels_short))
    decomp_plot_values = [float(v) if (v is not None and not (isinstance(v, float) and np.isnan(v))) else 0.0 for v in decomp_vals]
    ax2.bar(x2, decomp_plot_values, color=decomp_colors)
    ax2.set_title("Decomposition (years)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Years", fontsize=10)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(labels_short, rotation=30, ha="right", fontsize=9)
    ax2.tick_params(axis="y", labelsize=9)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

# ------------------------------
# Summary card (below)
# ------------------------------
new_co2_values = []
new_decomp_values = []
for i in range(1, 4):
    if pd.notna(row.get(f"New_CO2_{i}")):
        try:
            new_co2_values.append(float(row.get(f"New_CO2_{i}")))
        except:
            pass
    d = row.get(f"New_Decomposition_{i}")
    y = convert_to_years(d)
    if y is not None:
        new_decomp_values.append(y)

st.markdown("### 📘 Summary")
if len(new_co2_values) > 0:
    avg_new_co2 = sum(new_co2_values) / len(new_co2_values)
    old_co2_val = co2_old if not (isinstance(co2_old, float) and np.isnan(co2_old)) else avg_new_co2
    reduction_pct = round(((old_co2_val - avg_new_co2) / old_co2_val) * 100, 2) if old_co2_val != 0 else 0.0
    st.markdown(
        f"""
        <div class="summary-card">
        🌱 Switching from <b>{row.get('Old_Packaging')}</b> to the shown eco options reduces CO₂ by <b>{reduction_pct}%</b> on average.<br>
        Old CO₂: <b>{old_co2_val}</b> kg/kg → New average: <b>{avg_new_co2:.2f}</b> kg/kg
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("No CO₂ data for the eco-friendly alternatives to compute a CO₂ summary.")

if len(new_decomp_values) > 0:
    avg_new_decomp = sum(new_decomp_values) / len(new_decomp_values)
    old_decomp_val = convert_to_years(row.get("Old_Decomposition"))
    st.write(f"♻️ Old decomposition: **{row.get('Old_Decomposition', 'N/A')}**")
    st.write(f"♻️ Average decomposition of alternatives: **{avg_new_decomp:.2f} years**")
