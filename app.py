import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard")

df = pd.read_csv("data/sales.csv")

df["Revenue"] = df["Quantity"] * df["Price"]

st.title("Sales Intelligence Dashboard")
st.sidebar.header("Filters")
region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].unique())
)

if region != "All":
    df = df[df["Region"] == region]

product = st.sidebar.selectbox(
    "Select Product",
    ["All"] + list(df["Product"].unique())
)

if product != "All":
    df = df[df["Product"] == product]

total_revenue = df["Revenue"].sum()
total_orders = len(df)
average_order_value = total_revenue / total_orders if total_orders > 0 else 0

if len(df) > 0:
    top_product = (
        df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )
else:
    top_product = "N/A"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,}")
col2.metric("Total Orders", total_orders)
col3.metric("Top Product", top_product)
col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

st.subheader("Sales Data")

st.write(f"Showing {len(df)} records")

st.dataframe(df)

product_sales = (
    df.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    product_sales,
    x="Product",
    y="Revenue",
    title="Revenue By Product"
)
st.plotly_chart(fig1, use_container_width=True)


region_sales = (
    df.groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    region_sales,
    names="Region",
    values="Revenue",
    title="Revenue By Region"
)

st.plotly_chart(fig2, use_container_width=True)
df["Date"] = pd.to_datetime(df["Date"])

monthly_sales = (
    df.groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="Date",
    y="Revenue",
    title="Revenue Trend"
)

st.plotly_chart(fig3, use_container_width=True)
st.download_button(
    label="Download Sales Data",
    data=df.to_csv(index=False),
    file_name="sales_data.csv",
    mime="text/csv"
)