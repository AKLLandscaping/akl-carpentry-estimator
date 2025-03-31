import streamlit as st
import pandas as pd

# Updated material data from Renovation Quote Template
materials = [
    {"Category": "Delivery", "Item": "Delivery", "Unit": "per delivery", "Unit Price": 200.0},
    {"Category": "Demo", "Item": "Demo Cost", "Unit": "per sq.ft", "Unit Price": 6.0},
    {"Category": "Demo", "Item": "Permit", "Unit": "per item", "Unit Price": 500.0},
    {"Category": "Demo", "Item": "Bin Rental", "Unit": "per quote", "Unit Price": 600.0},
    {"Category": "Demo", "Item": "Garbage Bags", "Unit": "per box", "Unit Price": 26.98},
    {"Category": "Demo", "Item": "Fastener Charge", "Unit": "per job", "Unit Price": 500.0},
    {"Category": "Demo", "Item": "Equipment Rental", "Unit": "per quote", "Unit Price": 550.0},
    {"Category": "Framing", "Item": "2x4x8", "Unit": "each", "Unit Price": 4.5},
    {"Category": "Framing", "Item": "2x4x10", "Unit": "each", "Unit Price": 6.98},
    {"Category": "Framing", "Item": "2x4x12", "Unit": "each", "Unit Price": 8.38},
    {"Category": "Interior", "Item": "Drywall 1/2\" 4x8", "Unit": "per sheet", "Unit Price": 12.0},
    {"Category": "Interior", "Item": "Insulation Roll", "Unit": "each", "Unit Price": 40.0},
    {"Category": "Interior", "Item": "Laminate Flooring", "Unit": "per sq ft", "Unit Price": 2.5},
    {"Category": "Interior", "Item": "Interior Door", "Unit": "each", "Unit Price": 150.0},
    {"Category": "Interior", "Item": "Paint (gallon)", "Unit": "per gallon", "Unit Price": 30.0},
]

materials_df = pd.DataFrame(materials)

st.set_page_config(page_title="AKL Carpentry Estimator", layout="wide")
st.title("🔨 AKL Carpentry Estimator")

st.markdown("Estimate material costs for framing, demolition, equipment, drywall, and more.")

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
if "Lumber" in item or "2x4" in item:
    length_input = st.number_input("Length (ft)", min_value=1, value=8)

quantity = st.number_input("Quantity", min_value=1, value=1)

# Total cost
if "Lumber" in item or "2x4" in item:
    total = length_input * quantity * unit_price
else:
    total = quantity * unit_price

st.write(f"**Unit Price:** ${unit_price:.2f} ({unit})")
st.write(f"**Total Cost:** ${total:.2f}")

if st.button("➕ Add to Estimate"):
    st.session_state.summary.append({
        "Category": category,
        "Item": item,
        "Length (ft)": length_input if "Lumber" in item or "2x4" in item else "N/A",
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
