import streamlit as st
import pandas as pd

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Book Dashboard", layout="wide")

st.title("📊 Book Price Dashboard")

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("data.csv")

# -----------------------
# CLEAN DATA
# -----------------------
df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df = df.dropna()

# -----------------------
# METRICS SECTION
# -----------------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Price", f"₹{df['Price'].mean():.2f}")
col2.metric("Max Price", f"₹{df['Price'].max():.2f}")
col3.metric("Min Price", f"₹{df['Price'].min():.2f}")

# -----------------------
# FILTER SECTION
# -----------------------
st.subheader("🔍 Filter Books")

min_price = float(df["Price"].min())
max_price = float(df["Price"].max())

price_range = st.slider(
    "Select Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

filtered_df = df[
    (df["Price"] >= price_range[0]) &
    (df["Price"] <= price_range[1])
]

# -----------------------
# SORT DATA
# -----------------------
filtered_df = filtered_df.sort_values(by="Price", ascending=False)

# -----------------------
# DISPLAY TABLE (₹ FORMAT)
# -----------------------
st.subheader("📚 Data Preview")

df_display = filtered_df.copy()
df_display["Price"] = df_display["Price"].apply(lambda x: f"₹{x:.2f}")

st.dataframe(df_display, use_container_width=True)

# -----------------------
# CHART
# -----------------------
st.subheader("📊 Price Distribution")

st.bar_chart(filtered_df.set_index("Title")["Price"])