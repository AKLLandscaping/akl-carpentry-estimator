import streamlit as st
import pandas as pd

# Load sample material data (replace with live Kent.ca data when available)
data = [
    {"Category": "Framing", "Item": "2x4 PT Lumber", "Unit": "per ft", "Unit Price": 1.50},
    {"Category": "Framing", "Item": "2x6 KD Lumber", "Unit": "per ft", "Unit Price": 1.75},
    {"Category": "Framing", "Item": "OSB Sheathing 4x8", "Unit": "per sheet", "Unit Price": 25.00},
    {"Category": "Exterior", "Item": "Vinyl Siding Panel", "Unit": "each", "Unit Price": 14.00},
    {"Category": "Exterior", "Item": "Asphalt Shingles Bundle", "Unit": "per bundle", "Unit Price": 38.00},
    {"Category": "Interior", "Item": "Drywall 1/2\" 4x8", "Unit": "per sheet", "Unit Price": 12.00},
    {"Category": "Interior", "Item": "Insulation Roll", "Unit": "each", "Unit Price": 40.00},
    {"Category": "Interior", "Item": "Laminate Flooring", "Unit": "per sq ft", "Unit Price": 2.50},
    {"Category": "Interior", "Item": "Interior Door", "Unit": "each", "Unit Price": 150.00},
    {"Category": "Interior", "Item": "Paint (gallon)", "Unit": "per gallon", "Unit Price": 30.00},
]

materials_df = pd.DataFrame(data)

st.set_page_config(page_title="AKL Carpentry Estimator", layout="wide")
st.title("🔨 AKL Carpentry Estimator")

st.markdown("Estimate material costs for framing, siding, drywall, flooring, and more.")

# Initialize session state for summary if not already
if "summary" not in st.session_state:
    st.session_state.summary = []

# --- Input Section ---
category = st.selectbox("Select Material Category", materials_df["Category"].unique())
filtered_items = materials_df[materials_df["Category"] == category]
item = st.selectbox("Select Item", filtered_items["Item"])

selected_row = filtered_items[filtered_items["Item"] == item].iloc[0]
unit_price = selected_row["Unit Price"]
unit = selected_row["Unit"]

length_input = 0
if "Lumber" in item:
    length_input = st.number_input("Length (ft)", min_value=1, value=8)

quantity = st.number_input("Quantity", min_value=1, value=1)

# Total cost
if "Lumber" in item:
    total = length_input * quantity * unit_price
else:
    total = quantity * unit_price

st.write(f"**Unit Price:** ${unit_price:.2f} ({unit})")
st.write(f"**Total Cost:** ${total:.2f}")

if st.button("➕ Add to Estimate"):
    st.session_state.summary.append({
        "Category": category,
        "Item": item,
        "Length (ft)": length_input if "Lumber" in item else "N/A",
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Total": total
    })

# --- Summary Table ---
st.subheader("📋 Estimate Summary")

if st.session_state.summary:
    summary_df = pd.DataFrame(st.session_state.summary)
    st.dataframe(summary_df, use_container_width=True)
    grand_total = summary_df["Total"].sum()
    st.markdown(f"### 💰 Grand Total: ${grand_total:.2f}")
else:
    st.info("No materials added yet.")
