import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load data
conn = sqlite3.connect("data/superstore.db")
df = pd.read_sql("SELECT * FROM orders", conn)
conn.close()

# Header
st.title("🛒 Global Superstore Sales Analysis")
st.markdown("---")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales",   f"${df['sales'].sum()/1e6:.2f}M")
col2.metric("Total Profit",  f"${df['profit'].sum()/1e6:.2f}M")
col3.metric("Profit Margin", f"{df['profit'].sum()/df['sales'].sum()*100:.1f}%")
col4.metric("Total Orders",  f"{df['order_id'].nunique():,}")

st.markdown("---")

# Line Chart
df["order_date"] = pd.to_datetime(df["order_date"])
monthly = df.groupby(df["order_date"].dt.to_period("M")).agg(
    sales=("sales","sum")
).reset_index()
monthly["order_date"] = monthly["order_date"].dt.to_timestamp()

fig1 = px.line(monthly, x="order_date", y="sales",
               title="Monthly Revenue Trend",
               color_discrete_sequence=["#1F4E79"])
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart Sub-Category
sub = df.groupby("sub_category")["profit"].sum().reset_index()
sub = sub.sort_values("profit")
sub["color"] = sub["profit"].apply(
    lambda x: "#E74C3C" if x < 0 else "#2E75B6"
)
fig2 = px.bar(sub, x="profit", y="sub_category",
              title="Profit by Sub-Category",
              color="color",
              color_discrete_map="identity",
              orientation="h")
st.plotly_chart(fig2, use_container_width=True)

# RFM Segments
rfm = pd.read_csv("data/rfm_segments.csv")
col1, col2 = st.columns(2)

with col1:
    seg_count = rfm.groupby("RFM_Segment").size().reset_index(name="count")
    fig3 = px.pie(seg_count, names="RFM_Segment", values="count",
                  title="Customer Segment Distribution",
                  hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    seg_rev = rfm.groupby("RFM_Segment")["monetary"].sum().reset_index()
    fig4 = px.bar(seg_rev.sort_values("monetary"),
                  x="monetary", y="RFM_Segment",
                  title="Revenue by Segment",
                  orientation="h",
                  color_discrete_sequence=["#1F4E79"])
    st.plotly_chart(fig4, use_container_width=True)