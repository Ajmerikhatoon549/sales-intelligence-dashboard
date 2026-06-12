import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Page Config
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# Database Connection
conn = sqlite3.connect("sales.db")

df = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

# Revenue Calculation
df["Revenue"] = df["Quantity"] * df["Price"]

# Dashboard Title
st.title("📊 Sales Intelligence Dashboard")

# Sidebar Filters
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

# KPIs
total_revenue = df["Revenue"].sum()
total_orders = len(df)

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

if len(df) > 0:

    top_product = (
        df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )

    best_region = (
        df.groupby("Region")["Revenue"]
        .sum()
        .idxmax()
    )

else:
    top_product = "N/A"
    best_region = "N/A"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Total Orders",
    total_orders
)

col3.metric(
    "Top Product",
    top_product
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col5.metric(
    "Best Region",
    best_region
)

# Data Table
st.subheader("Sales Data")

st.write(f"Showing {len(df)} records")

st.dataframe(
    df,
    use_container_width=True
)

# Revenue by Product
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

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Revenue by Region
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

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Revenue Trend
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

st.plotly_chart(
    fig3,
    use_container_width=True
)

# Monthly Revenue Analysis
df["Month"] = df["Date"].dt.strftime("%Y-%m")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    monthly_revenue,
    x="Month",
    y="Revenue",
    title="Monthly Revenue Analysis",
    markers=True
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# Top 5 Products
top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig5 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    title="Top 5 Products by Revenue"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# Region Performance
st.subheader("Region Performance")

region_performance = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(
    region_performance,
    use_container_width=True
)

# Download Button
st.download_button(
    label="📥 Download Sales Data",
    data=df.to_csv(index=False),
    file_name="sales_data.csv",
    mime="text/csv"
)

# Close DB Connection
conn.close()