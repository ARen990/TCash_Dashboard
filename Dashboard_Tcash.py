import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="University Course Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #748DAE;   /* สีพื้นหลังเว็บ */
    }
    [data-testid="stSidebar"] {
        background-color: #9ECAD6;   /* สี Sidebar */
    }
    </style>
""", unsafe_allow_html=True)

# Load data
with open(r"D:\\Y3\\J.bod\data\data_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["ค่าใช้จ่าย"] = pd.to_numeric(df["ค่าใช้จ่าย"], errors="coerce")
# st.title("🎓 University Course Dashboard")

# ---------------------- Create a page select button ----------------------

page = st.sidebar.selectbox(
    "MENU",
    ["Dashboard", "Find Tuition Fees", "Course search table"]
)

# ---------------------- Add a Dashboard page ----------------------
if page == "Dashboard":

    st.title("📊 Dashboard")

    # ----- Summary Card -----
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of universities", df["มหาวิทยาลัย"].nunique())
    col2.metric("Total number of courses", len(df))
    col3.metric("Total average expenses (baht)", f"{df['ค่าใช้จ่าย'].mean():,.0f}")

        # --- pie graph and his ---

    # --- pie graph and his ---
    faculty_count = df['คณะ'].value_counts().head(5)
    col1, col2 = st.columns([1, 2])

    with col1:
        fig = px.histogram(df, x='ค่าใช้จ่าย', nbins=20, 
                            title='Distribution of costs',
                            color_discrete_sequence=["#9ECAD6", "#F5CBCB"],
                            )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=16, color="#FFFFFF")
            )   
        st.plotly_chart(fig)

    with col2:
        fig = px.pie(
            values=faculty_count.values,
            names=faculty_count.index,
            title='Figure of faculty numbers (Top 5)',
            color_discrete_sequence=["#9ECAD6", "#F5CBCB"],
            # hole=0.3
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=16, color="#FFFFFF")
            )  
        st.plotly_chart(fig, use_container_width=True)

    # --- bar top 5 ---
    st.subheader("Top 5 The most expensive and the cheapest")
    cost_mean = df.groupby("มหาวิทยาลัย")["ค่าใช้จ่าย"].mean().dropna()
    top5 = cost_mean.sort_values(ascending=False).head(5)
    low5 = cost_mean.sort_values(ascending=True).head(5)
    combined = pd.concat([top5, low5])

    fig = px.bar(
        combined,
        x=combined.values,
        y=combined.index,
        color=["Most expensive"] * len(top5) + ["Cheapest"] * len(low5),
        orientation="h",
        text_auto=True,
        labels={"x": "Average cost (baht)", "y": "University"},
        color_discrete_sequence=["#9ECAD6", "#F5CBCB"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=16, color="#FFFFFF")
        )   

    st.plotly_chart(fig, use_container_width=True)

    # --- bar top 5 ---
    st.subheader("Top 10 Most university courses")
    uni_count = df["มหาวิทยาลัย"].value_counts().head(10)
    fig1 = px.bar(uni_count, x=uni_count.index, 
                    y=uni_count.values, 
                    labels={"x": "University", "y": "Number of courses"},
                    color_discrete_sequence=["#9ECAD6", "#F5CBCB"],
                    )
    fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(size=16, color="#FFFFFF")
    )   
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------- เพิ่มหน้า Dashboard ----------------------
elif page == "Find Tuition Fees":

    st.title("🔍 Find some tuition fees")

# ---------------------- หน้า Course search table ----------------------
elif page == "Course search table":

    st.title("📋 Course search table")