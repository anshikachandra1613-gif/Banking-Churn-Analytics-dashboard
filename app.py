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
df = pd.read_excel("data/European_Bank.xlsx")


# Sidebar filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Geography", ["All"] + df["Geography"].unique().tolist())
selected_age = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))

# Apply filters
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["Geography"] == selected_country]
filtered_df = filtered_df[(filtered_df["Age"] >= selected_age[0]) & (filtered_df["Age"] <= selected_age[1])]


# --- KPI Section at Top ---
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .kpi-title {
        font-size: 16px;
        font-weight: bold;
        color: #003366; /* Navy Blue */
    }
    .kpi-value {
        font-size: 20px;
        font-weight: bold;
        color: #006400; /* Deep Green */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Key Performance Indicators (KPIs)")

overall_churn_rate = filtered_df["Exited"].mean() * 100
segment_churn = filtered_df.groupby("Geography")["Exited"].mean().mean() * 100
high_value = filtered_df[filtered_df["Balance"] > 100000]
high_value_churn_ratio = high_value["Exited"].mean() * 100
geo_risk_index = filtered_df.groupby("Geography")["Exited"].mean().max() * 100
inactive_churn = filtered_df[filtered_df["IsActiveMember"] == 0]["Exited"].mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📉 Overall Churn Rate</div><div class='kpi-value'>{overall_churn_rate:.2f}%</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📊 Segment Churn Rate</div><div class='kpi-value'>{segment_churn:.2f}%</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>⭐ High-Value Churn Ratio</div><div class='kpi-value'>{high_value_churn_ratio:.2f}%</div></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>🌍 Geographic Risk Index</div><div class='kpi-value'>{geo_risk_index:.2f}%</div></div>", unsafe_allow_html=True)

with col5:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>⚡ Engagement Drop Indicator</div><div class='kpi-value'>{inactive_churn:.2f}%</div></div>", unsafe_allow_html=True)


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


import streamlit as st
import pandas as pd

# --- Step 1: Data Readiness Overview ---
st.header("Data Readiness & Validation")

# Load dataset
df = pd.read_excel("data/European_Bank.xlsx")

# Perform validation checks (internal, not shown directly)
overall_churn_rate = df["Exited"].mean() * 100
binary_cols = ["Exited", "IsActiveMember"]
binary_check = all(df[col].dropna().isin([0,1]).all() for col in binary_cols if col in df.columns)
engagement_check = "IsActiveMember" in df.columns and "NumOfProducts" in df.columns
churn_check = set(df["Exited"].unique()).issubset({0,1})

# Compute Data Quality Score
checks_passed = sum([binary_check, engagement_check, churn_check])
total_checks = 3
data_quality_score = (checks_passed / total_checks) * 100

# Professional summary card
st.markdown(
    f"""
    <div style='background-color:#E6F4EA;padding:15px;border-radius:8px;
    text-align:center;box-shadow:0 2px 4px rgba(0,0,0,0.1);'>
        <h4 style='color:#003366;'>📂 Data Readiness Overview</h4>
        <p style='color:#2E8B57;font-size:18px;font-weight:bold;'>Integrity Status: Ready</p>
        <p style='color:#006400;'>Data Quality Score: {data_quality_score:.0f}%</p>
        <p style='color:#555;'>Dataset validated for engagement fields, binary consistency, and churn labeling.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Step 2: Data Cleaning & Preparation ---


# 1. Remove non-analytical fields
if "Surname" in df.columns:
    df = df.drop(columns=["Surname"])

# 2. Convert categorical variables for grouping
categorical_cols = ["Geography", "Gender"]
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype("category")

# 3. Create derived segmentation fields
df["CustomerSegment"] = pd.cut(df["Balance"], bins=[-1, 50000, 100000, 200000], labels=["Low", "Medium", "High"])
df["AgeGroup"] = pd.cut(df["Age"], bins=[17, 30, 45, 60, 100], labels=["Young", "Adult", "Mature", "Senior"])


# --- Step 7: Customer Segmentation Design ---
st.header("Customer Segmentation Design")

# --- KPI Section: Customer Segmentation Design ---
st.subheader("Segmentation KPIs (Key Highlights)")

# Calculate key KPIs
geo_top = filtered_df["Geography"].value_counts().idxmax()
geo_top_count = filtered_df["Geography"].value_counts().max()

age_groups = pd.cut(filtered_df["Age"], bins=[0,30,45,60,120], labels=["<30","30-45","46-60","60+"])
age_top = age_groups.value_counts().idxmax()
age_top_count = age_groups.value_counts().max()

credit_bands = pd.cut(filtered_df["CreditScore"], bins=[0,500,700,1000], labels=["Low","Medium","High"])
credit_top = credit_bands.value_counts().idxmax()
credit_top_count = credit_bands.value_counts().max()

balance_groups = pd.cut(filtered_df["Balance"], bins=[-1,1,50000,filtered_df["Balance"].max()],
                        labels=["Zero-balance","Low-balance","High-balance"])
balance_zero = balance_groups.value_counts()["Zero-balance"]
balance_high = balance_groups.value_counts()["High-balance"]

# Attractive KPI cards
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #fdfdfd;
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 5px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: bold;
        color: #444;
    }
    .kpi-value {
        font-size: 18px;
        font-weight: bold;
        color: #2E8B57;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>🌍 Top Geography</div><div class='kpi-value'>{geo_top} ({geo_top_count})</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>👤 Largest Age Group</div><div class='kpi-value'>{age_top} ({age_top_count})</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>💳 Dominant Credit Band</div><div class='kpi-value'>{credit_top} ({credit_top_count})</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>💰 Balance Snapshot</div><div class='kpi-value'>Zero: {balance_zero}, High: {balance_high}</div></div>", unsafe_allow_html=True)


# --- Geographic Segmentation (France, Spain, Germany) → Horizontal Bar ---
st.subheader("Geographic Segmentation")
geo_counts = filtered_df["Geography"].value_counts().reset_index()
geo_counts.columns = ["Geography","Count"]
fig_geo = px.bar(
    geo_counts, x="Count", y="Geography", orientation="h",
    color="Geography", text="Count",
    title="Customer Distribution by Geography",
    color_discrete_sequence=["#003366","#87CEFA","#FF69B4"]
)
st.plotly_chart(fig_geo, use_container_width=True)

# --- Age Segmentation (<30, 30–45, 46–60, 60+) → Stacked Column ---
st.subheader("Age Segmentation")
age_groups = pd.cut(filtered_df["Age"], bins=[0,30,45,60,120], labels=["<30","30-45","46-60","60+"])
age_churn = pd.crosstab(age_groups, filtered_df["Exited"]).reset_index()
fig_age = px.bar(
    age_churn, x="Age", y=[0,1],
    barmode="stack", title="Age Segmentation vs Churn",
    labels={"value":"Customers","variable":"Exited"},
    color_discrete_map={0:"green",1:"red"}
)
st.plotly_chart(fig_age, use_container_width=True)

# --- Credit Score Bands (Low, Medium, High) → Lollipop Chart ---
st.subheader("Credit Score Segmentation")
credit_bands = pd.cut(filtered_df["CreditScore"], bins=[0,500,700,1000], labels=["Low","Medium","High"])
credit_counts = credit_bands.value_counts().reset_index()
credit_counts.columns = ["Credit Band","Count"]
fig_credit = px.scatter(
    credit_counts, x="Credit Band", y="Count", size="Count",
    color="Credit Band", title="Credit Score Segmentation (Lollipop Style)",
    color_discrete_sequence=["#FFD700","#4682B4","#FF69B4"]
)
fig_credit.update_traces(mode="markers+lines")
st.plotly_chart(fig_credit, use_container_width=True)

# --- Tenure Groups (New, Mid-term, Long-term) → Heatmap ---
st.subheader("Tenure Groups")
tenure_groups = pd.cut(filtered_df["Tenure"], bins=[-1,3,7,15], labels=["New","Mid-term","Long-term"])
tenure_churn = pd.crosstab(tenure_groups, filtered_df["Exited"])
fig_tenure = px.imshow(
    tenure_churn, text_auto=True, color_continuous_scale="YlGnBu",
    title="Tenure Groups vs Churn"
)
st.plotly_chart(fig_tenure, use_container_width=True)

# --- Balance Segments (Zero, Low, High) → Donut Chart ---
st.subheader("Balance Segmentation")
balance_groups = pd.cut(filtered_df["Balance"], bins=[-1,1,50000,filtered_df["Balance"].max()],
                        labels=["Zero-balance","Low-balance","High-balance"])
balance_counts = balance_groups.value_counts().reset_index()
balance_counts.columns = ["Balance Group","Count"]
fig_balance = px.pie(
    balance_counts, names="Balance Group", values="Count",
    hole=0.4, title="Balance Segmentation",
    color="Balance Group", color_discrete_sequence=["#6A5ACD","#20B2AA","#FF8C00"]
)
st.plotly_chart(fig_balance, use_container_width=True)


# --- Churn Distribution Analysis ---
st.header("Churn Distribution Analysis")

# --- KPI Section: Churn Distribution Analysis ---
st.header("Key Performance Indicators (KPIs)")

# Custom CSS for attractive KPI cards
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #fdfdfd; /* very light background */
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin: 5px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: bold;
        color: #2F4F4F; /* dark slate gray */
    }
    .kpi-value {
        font-size: 16px;
        font-weight: bold;
        color: #4682B4; /* steel blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Calculate KPIs
churned_customers = filtered_df[filtered_df["Exited"] == 1].shape[0]
retained_customers = filtered_df[filtered_df["Exited"] == 0].shape[0]
avg_credit_churned = filtered_df[filtered_df["Exited"] == 1]["CreditScore"].mean()
avg_credit_retained = filtered_df[filtered_df["Exited"] == 0]["CreditScore"].mean()

# Display KPIs in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>🚨 Churned Customers</div><div class='kpi-value'>{churned_customers}</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>✅ Retained Customers</div><div class='kpi-value'>{retained_customers}</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📊 Avg Credit (Churned)</div><div class='kpi-value'>{avg_credit_churned:.1f}</div></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>⭐ Avg Credit (Retained)</div><div class='kpi-value'>{avg_credit_retained:.1f}</div></div>", unsafe_allow_html=True)


# --- Geography vs Churn (Treemap) ---
st.header("Geography-wise Churn")
geo_churn = filtered_df.groupby("Geography")["Exited"].mean().reset_index()
fig_geo = px.treemap(
    geo_churn, path=["Geography"], values="Exited",
    color="Exited", color_continuous_scale="RdBu",
    title="Churn Rate by Geography (Treemap)"
)
st.plotly_chart(fig_geo, use_container_width=True)

# --- Age vs Churn (Box Plot instead of violin) ---
st.header("Age Distribution of Churn")
fig_age = px.box(
    filtered_df, x="Exited", y="Age",
    color="Exited", color_discrete_map={0:"green", 1:"red"},
    title="Age Comparison: Churned vs Retained"
)
st.plotly_chart(fig_age, use_container_width=True)

# --- Tenure vs Churn (Scatter) ---
st.header("Tenure vs Churn Rate")
tenure_churn = filtered_df.groupby("Tenure")["Exited"].mean().reset_index()
fig_tenure = px.scatter(
    tenure_churn, x="Tenure", y="Exited",
    size="Exited", color="Exited",
    title="Churn Rate vs Tenure (Scatter)"
)
st.plotly_chart(fig_tenure, use_container_width=True)

# --- High-Value Customer Analysis (Sunburst) ---
st.header("High-Value Customer Churn")
high_value = filtered_df[filtered_df["Balance"] > 100000]
hv_churn_rate = high_value["Exited"].mean() * 100
st.metric("High-Value Churn Rate (%)", f"{hv_churn_rate:.2f}")

fig_hv = px.sunburst(
    high_value, path=["Geography","Exited"],
    title="High-Value Customer Churn (Sunburst)",
    color="Exited", color_discrete_map={0:"green", 1:"red"}
)
st.plotly_chart(fig_hv, use_container_width=True)

# --- Overall Churn Rate ---
overall_churn = filtered_df["Exited"].mean() * 100
total_customers = len(filtered_df)
churned_customers = filtered_df[filtered_df["Exited"] == 1].shape[0]

col1, col2 = st.columns(2)
col1.metric("Total Customers", total_customers)
col2.metric("Overall Churn Rate (%)", f"{overall_churn:.2f}")

# --- Segment-wise Churn Rates ---
st.header("Segment-wise Churn Rates")
segment_churn = filtered_df.groupby("Geography")["Exited"].mean().reset_index()
fig_segment = px.bar(
    segment_churn, x="Geography", y="Exited",
    title="Churn Rate by Geography",
    color="Exited", color_continuous_scale="Blues"
)
st.plotly_chart(fig_segment, use_container_width=True)

# --- Churn Contribution by Segment Size ---
st.header("Churn Contribution by Segment Size")
age_groups = pd.cut(filtered_df["Age"], bins=[0,30,45,60,120], labels=["<30","30-45","46-60","60+"])
age_churn = pd.crosstab(age_groups, filtered_df["Exited"]).reset_index()
fig_contrib = px.bar(
    age_churn, x="Age", y=[0,1],
    title="Churn Contribution by Age Segment",
    barmode="stack", labels={"value":"Customers","variable":"Exited"}
)
st.plotly_chart(fig_contrib, use_container_width=True)

# --- Comparison of Churned vs Retained Profiles ---
st.header("Comparison of Churned vs Retained Profiles")
profile_vars = ["Age","Balance","CreditScore","Tenure"]
profile_means = filtered_df.groupby("Exited")[profile_vars].mean().reset_index()
fig_profiles = px.line(
    profile_means.melt(id_vars="Exited", value_vars=profile_vars),
    x="variable", y="value", color="Exited",
    markers=True, title="Profiles: Churned vs Retained"
)
st.plotly_chart(fig_profiles, use_container_width=True)


# --- Step 5: Comparative Demographic Analysis ---
st.header("Comparative Demographic Analysis")

# --- KPI Section (Styled Cards) ---
st.subheader("Key Demographic KPIs")

# Calculate KPIs
churned_male = filtered_df[(filtered_df["Gender"]=="Male") & (filtered_df["Exited"]==1)].shape[0]
churned_female = filtered_df[(filtered_df["Gender"]=="Female") & (filtered_df["Exited"]==1)].shape[0]
avg_credit_churned = filtered_df[filtered_df["Exited"]==1]["CreditScore"].mean()
avg_credit_retained = filtered_df[filtered_df["Exited"]==0]["CreditScore"].mean()

# Custom CSS for attractive KPI cards
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #fdfdfd;
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 5px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: bold;
        color: #444;
    }
    .kpi-value {
        font-size: 18px;
        font-weight: bold;
        color: #2E8B57; /* sea green accent */
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>👨 Churned Males</div><div class='kpi-value'>{churned_male}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>👩 Churned Females</div><div class='kpi-value'>{churned_female}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📊 Avg Credit (Churned)</div><div class='kpi-value'>{avg_credit_churned:.1f}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>⭐ Avg Credit (Retained)</div><div class='kpi-value'>{avg_credit_retained:.1f}</div></div>", unsafe_allow_html=True)

# --- Gender-based Churn Differences (Donut Chart) ---
st.header("Gender-based Churn Differences")
gender_churn = filtered_df.groupby("Gender")["Exited"].mean().reset_index()
fig_gender = px.pie(
    gender_churn, names="Gender", values="Exited",
    hole=0.4, title="Churn Rate by Gender (Donut)",
    color="Gender", color_discrete_map={"Male":"#4682B4","Female":"#FF69B4"}
)
st.plotly_chart(fig_gender, use_container_width=True)

# --- Geography-Age Interaction (Bubble Chart) ---
st.header("Geography-Age Interaction Analysis")
geo_age = filtered_df.groupby(["Geography","Age"])["Exited"].mean().reset_index()
fig_geo_age = px.scatter(
    geo_age, x="Age", y="Exited", size="Exited",
    color="Geography", title="Age vs Churn Rate by Geography (Bubble Chart)"
)
st.plotly_chart(fig_geo_age, use_container_width=True)

# --- Financial Stability vs Churn (Stacked Area Chart) ---
st.header("Financial Stability vs Churn Comparison")
filtered_df["BalanceGroup"] = pd.cut(
    filtered_df["Balance"], bins=[-1,1,50000,100000,filtered_df["Balance"].max()],
    labels=["Zero","Low","Medium","High"]
)
balance_churn = pd.crosstab(filtered_df["BalanceGroup"], filtered_df["Exited"]).reset_index()
fig_balance = px.area(
    balance_churn, x="BalanceGroup", y=[0,1],
    title="Churn vs Retained by Financial Stability",
    labels={"value":"Customers","variable":"Exited"},
    color_discrete_map={0:"green",1:"red"}
)
st.plotly_chart(fig_balance, use_container_width=True)


# --- Step 6: High-Value Customer Churn Analysis ---
st.header("High-Value Customer Churn Analysis")

# --- KPI Section (Styled Cards) ---
st.subheader("Key High-Value KPIs")

# Calculate KPIs
high_value = filtered_df[filtered_df["Balance"] > 100000]
hv_churned = high_value[high_value["Exited"]==1].shape[0]
hv_retained = high_value[high_value["Exited"]==0].shape[0]
avg_salary_churned = high_value[high_value["Exited"]==1]["EstimatedSalary"].mean()
revenue_risk = high_value[high_value["Exited"]==1]["Balance"].sum()

# Custom CSS for attractive KPI cards
st.markdown(
    """
    <style>
    .kpi-card {
        background-color: #fdfdfd;
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 5px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: bold;
        color: #444;
    }
    .kpi-value {
        font-size: 18px;
        font-weight: bold;
        color: #B22222; /* firebrick accent */
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>💰 High-Value Churned</div><div class='kpi-value'>{hv_churned}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>🔒 High-Value Retained</div><div class='kpi-value'>{hv_retained}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📊 Avg Salary (Churned)</div><div class='kpi-value'>{avg_salary_churned:.0f}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>⚠️ Revenue Risk</div><div class='kpi-value'>{revenue_risk:,.0f}</div></div>", unsafe_allow_html=True)

# --- Identify High-Balance Churners (Treemap) ---
st.header("High-Balance Churners by Geography")
fig_hv_geo = px.treemap(
    high_value, path=["Geography","Exited"], values="Balance",
    color="Exited", color_discrete_map={0:"green",1:"red"},
    title="High-Balance Churn Distribution"
)
st.plotly_chart(fig_hv_geo, use_container_width=True)

# --- Salary vs Balance Churn Patterns (Grouped Bar instead of bubble) ---
st.header("Salary vs Balance Churn Patterns")
salary_bins = pd.cut(high_value["EstimatedSalary"], bins=[0,50000,100000,150000,200000], labels=["<50k","50-100k","100-150k","150k+"])
salary_balance = high_value.groupby([salary_bins,"Exited"])["Balance"].mean().reset_index()
fig_salary_balance = px.bar(
    salary_balance, x="EstimatedSalary", y="Balance",
    color="Exited", barmode="group",
    title="Average Balance by Salary Group (Churned vs Retained)",
    color_discrete_map={0:"blue",1:"orange"}
)
st.plotly_chart(fig_salary_balance, use_container_width=True)

# --- Revenue Risk from Churn (Funnel Chart instead of bar) ---
st.header("Revenue Risk from Churn")
risk_data = pd.DataFrame({
    "Stage":["Total Balance","Retained Value","Churned Loss"],
    "Amount":[high_value["Balance"].sum(),
              high_value[high_value["Exited"]==0]["Balance"].sum(),
              high_value[high_value["Exited"]==1]["Balance"].sum()]
})
fig_risk = px.funnel(
    risk_data, x="Amount", y="Stage",
    title="Revenue Risk Funnel"
)
st.plotly_chart(fig_risk, use_container_width=True)

# --- Step: Model Evaluation & Performance (Fixed Weak Points) ---
st.header("Model Evaluation & Performance")

# --- Train-Test Split (Manual, no sklearn) ---
import numpy as np

# Features and target
X = filtered_df[["Age","Balance","CreditScore","Tenure","IsActiveMember","NumOfProducts"]].values
y = filtered_df["Exited"].values

# Manual split (70% train, 30% test)
split_idx = int(0.7 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# --- Simple Baseline Model: Predict majority class ---
majority_class = np.bincount(y_train).argmax()
y_pred_baseline = np.full_like(y_test, majority_class)

# --- Metrics (MSE, Accuracy) ---
mse_baseline = np.mean((y_test - y_pred_baseline)**2)
acc_baseline = np.mean(y_test == y_pred_baseline)

# --- KPI Cards for Metrics ---
st.subheader("Baseline Model KPIs")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>📉 MSE</div><div class='kpi-value bad'>{mse_baseline:.2f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>✅ Accuracy</div><div class='kpi-value good'>{acc_baseline:.2f}</div></div>", unsafe_allow_html=True)

# --- Confusion Matrix (Manual) ---
st.subheader("Confusion Matrix (Baseline)")
tp = np.sum((y_test==1) & (y_pred_baseline==1))
tn = np.sum((y_test==0) & (y_pred_baseline==0))
fp = np.sum((y_test==0) & (y_pred_baseline==1))
fn = np.sum((y_test==1) & (y_pred_baseline==0))
cm = np.array([[tn,fp],[fn,tp]])

fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                   x=["Pred Retained","Pred Churned"], y=["Actual Retained","Actual Churned"],
                   title="Confusion Matrix - Baseline Model")
st.plotly_chart(fig_cm, use_container_width=True)

# --- ROC Curve (Manual) ---
st.subheader("ROC Curve (Baseline)")
# For baseline, probability = proportion of churn in train
p_churn = np.mean(y_train)
y_prob = np.full_like(y_test, p_churn, dtype=float)

fpr = []
tpr = []
thresholds = np.linspace(0,1,50)
for thresh in thresholds:
    y_pred_thresh = (y_prob >= thresh).astype(int)
    tp = np.sum((y_test==1) & (y_pred_thresh==1))
    tn = np.sum((y_test==0) & (y_pred_thresh==0))
    fp = np.sum((y_test==0) & (y_pred_thresh==1))
    fn = np.sum((y_test==1) & (y_pred_thresh==0))
    fpr.append(fp/(fp+tn) if (fp+tn)>0 else 0)
    tpr.append(tp/(tp+fn) if (tp+fn)>0 else 0)

fig_roc = px.area(
    x=fpr, y=tpr, title=f"ROC Curve - Baseline Model",
    labels=dict(x="False Positive Rate", y="True Positive Rate"),
    color_discrete_sequence=["#B22222"]
)
fig_roc.add_shape(type='line', line=dict(dash='dash'), x0=0, x1=1, y0=0, y1=1)
st.plotly_chart(fig_roc, use_container_width=True)

# --- Problem Statement Alignment ---
st.header("📌 Problem Statement Alignment")

# Custom CSS for attractive alignment cards
st.markdown(
    """
    <style>
    .align-card {
        background-color: #f9f9f9;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 8px;
    }
    .align-title {
        font-size: 14px;
        font-weight: bold;
        color: #2F4F4F;
        margin-bottom: 6px;
    }
    .align-value {
        font-size: 13px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        "<div class='align-card'><div class='align-title'>🎯 High-Risk Segments</div><div class='align-value'>Identified via churn spotlight & segmentation analysis</div></div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='align-card'><div class='align-title'>🌍 Geography & Demographics</div><div class='align-value'>Differences shown through region & age segmentation visuals</div></div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        "<div class='align-card'><div class='align-title'>💰 Financial Profile</div><div class='align-value'>Churned vs retained customers compared on balance & salary</div></div>",
        unsafe_allow_html=True
    )


# --- Executive Summary for Government Stakeholders ---
st.header("📑 Executive Summary")

# Custom CSS for attractive summary card
st.markdown(
    """
    <style>
    .summary-card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        font-family: 'Segoe UI', sans-serif;
    }
    .summary-title {
        font-size: 18px;
        font-weight: bold;
        color: #2F4F4F;
        margin-bottom: 10px;
    }
    .summary-point {
        font-size: 14px;
        margin: 6px 0;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Executive Summary Content
summary_content = """
<div class='summary-card'>
    <div class='summary-title'>Key Insights for Policy Makers</div>
    <div class='summary-point'>• Churn among high‑value customers poses a significant revenue risk, requiring targeted retention programs.</div>
    <div class='summary-point'>• Geographic disparities (France, Spain, Germany) highlight the need for region‑specific engagement strategies.</div>
    <div class='summary-point'>• Age and tenure segmentation reveal vulnerable groups (young and new customers) that need early intervention.</div>
    <div class='summary-point'>• Financial stability indicators (balance and credit score) correlate strongly with churn, suggesting policy levers for financial literacy and support.</div>
    <div class='summary-point'>• Predictive analytics can guide resource allocation, ensuring government programs focus on at‑risk populations efficiently.</div>
</div>
"""

st.markdown(summary_content, unsafe_allow_html=True)

# --- Recommendations Matrix for Stakeholders ---
st.header("📊 Recommendations Matrix")

# Create matrix data
recommendations = pd.DataFrame({
    "Issue": [
        "High-value customer churn",
        "Geographic disparities (France, Spain, Germany)",
        "Young & new customers at risk",
        "Low credit score segments",
        "Zero-balance accounts"
    ],
    "Policy Action": [
        "Introduce targeted retention incentives & loyalty programs",
        "Develop region-specific outreach and engagement campaigns",
        "Provide early onboarding support & financial literacy workshops",
        "Offer credit improvement schemes & advisory services",
        "Encourage savings programs and balance-building initiatives"
    ],
    "Expected Outcome": [
        "Reduced revenue loss from churn",
        "Balanced customer retention across regions",
        "Lower churn among vulnerable age/tenure groups",
        "Improved financial stability & reduced churn risk",
        "Greater customer resilience and long-term retention"
    ]
})

# Display styled dataframe instead of go.Table
st.dataframe(recommendations.style
             .set_properties(**{'background-color': '#f9f9f9',
                                'color': '#333',
                                'border-color': 'white'})
             .set_table_styles([{
                 'selector': 'th',
                 'props': [('background-color', '#2F4F4F'),
                           ('color', 'white'),
                           ('font-weight', 'bold')]
             }]),
             use_container_width=True)
