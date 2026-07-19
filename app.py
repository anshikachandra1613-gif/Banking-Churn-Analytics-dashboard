import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard Title & Config
st.set_page_config(
    page_title="Customer Segmentation & Churn Pattern Analytics in European Banking Dashboard",
    layout="wide"
)

st.title("📊 Customer Segmentation & Churn Pattern Analytics in European Banking Dashboard")
st.markdown("This interactive dashboard highlights churn patterns, customer segmentation, and predictive insights across European banking customers.")

# Load dataset (Excel format)
df = pd.read_csv("European_Bank.csv")

# Sidebar filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Geography", ["All"] + df["Geography"].unique().tolist())
selected_age = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))

# Apply filters
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Geography"] == selected_country]
filtered_df = filtered_df[(filtered_df["Age"] >= selected_age[0]) & (filtered_df["Age"] <= selected_age[1])]

# --- Overall Churn Summary ---
st.header("Overall Churn Summary")
total_customers = len(filtered_df)
churn_rate = filtered_df["Exited"].mean() * 100
avg_balance_churned = filtered_df[filtered_df["Exited"] == 1]["Balance"].mean()
avg_balance_retained = filtered_df[filtered_df["Exited"] == 0]["Balance"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers)
col2.metric("Churn Rate (%)", f"{churn_rate:.2f}")
col3.metric("Avg Balance (Churned)", f"{avg_balance_churned:.2f}")
col4.metric("Avg Balance (Retained)", f"{avg_balance_retained:.2f}")

# --- Geography-wise Churn ---
st.header("Geography-wise Churn")
geo_churn = filtered_df.groupby("Geography")["Exited"].mean().reset_index()
fig_geo = px.bar(geo_churn, x="Geography", y="Exited", title="Churn Rate by Geography")
st.plotly_chart(fig_geo, use_container_width=True)

# --- Age & Tenure Comparison ---
st.header("Age & Tenure Churn Comparison")
fig_age = px.histogram(filtered_df, x="Age", color="Exited", barmode="group", title="Churn by Age")
st.plotly_chart(fig_age, use_container_width=True)

fig_tenure = px.line(
    filtered_df.groupby("Tenure")["Exited"].mean().reset_index(),
    x="Tenure", y="Exited", title="Churn Rate vs Tenure"
)
st.plotly_chart(fig_tenure, use_container_width=True)

# --- High-Value Customer Explorer ---
st.header("High-Value Customer Churn Explorer")
high_value = filtered_df[filtered_df["Balance"] > 100000]  # threshold example
hv_churn_rate = high_value["Exited"].mean() * 100
st.metric("High-Value Churn Rate (%)", f"{hv_churn_rate:.2f}")

fig_hv = px.pie(high_value, names="Exited", title="High-Value Customer Churn Distribution")
st.plotly_chart(fig_hv, use_container_width=True)
