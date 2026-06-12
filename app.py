import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard")

df = pd.read_csv("data/sales.csv")

df["Revenue"] = df["Quantity"] * df["Price"]

st.title("Sales Intelligence Dashboard")

total_revenue = df["Revenue"].sum()
total_orders = len(df)

col1, col2 = st.columns(2)

col1.metric("Total Revenue", f"₹{total_revenue:,}")
col2.metric("Total Orders", total_orders)

st.subheader("Sales Data")
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

st.plotly_chart(fig1)

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

st.plotly_chart(fig2)