
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sales Analysis Dashboard",
    layout="wide"
)

st.title("Sales Data Analysis and Prediction")
st.write("Interactive Business Sales Dashboard")

# Upload Excel or CSV dataset
uploaded_file = st.file_uploader(
    "Upload Superstore Sales Dataset",
    type=["xls", "xlsx", "csv"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df["Order Date"] = pd.to_datetime(
        df["Order Date"]
    )

    # Sidebar filters
    st.sidebar.header("Filters")

    categories = st.sidebar.multiselect(
        "Select Category",
        df["Category"].unique(),
        default=list(df["Category"].unique())
    )

    regions = st.sidebar.multiselect(
        "Select Region",
        df["Region"].unique(),
        default=list(df["Region"].unique())
    )

    filtered_df = df[
        df["Category"].isin(categories)
        & df["Region"].isin(regions)
    ]

    # Dashboard metrics
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Sales",
        f"${filtered_df['Sales'].sum():,.2f}"
    )

    c2.metric(
        "Total Profit",
        f"${filtered_df['Profit'].sum():,.2f}"
    )

    c3.metric(
        "Total Orders",
        filtered_df["Order ID"].nunique()
    )

    # Category chart
    st.subheader("Category-wise Sales")

    category_sales = filtered_df.groupby(
        "Category"
    )["Sales"].sum()

    st.bar_chart(category_sales)

    # Monthly chart
    st.subheader("Monthly Sales Trend")

    monthly = (
        filtered_df.set_index("Order Date")["Sales"]
        .resample("MS")
        .sum()
    )

    st.line_chart(monthly)

    # Data table
    st.subheader("Sales Data")
    st.dataframe(filtered_df.head(100))

else:
    st.info("Upload your Superstore dataset to view the dashboard.")
