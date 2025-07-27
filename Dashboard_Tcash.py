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

# ---------------------- Add a Find Tuition Fees  page ----------------------
elif page == "Find Tuition Fees":

    st.title("🔍 Find some tuition fees")

    # --- Find close expenses ---
    st.subheader("Find the course with the closest tuition fee")

    input_cost = st.number_input("Enter the number (baht)", min_value=0, step=1000)
    if input_cost > 0:
        df_sorted = df.sort_values("ค่าใช้จ่าย").dropna(subset=["ค่าใช้จ่าย"])
        df_sorted["ต่างจากที่กรอก"] = abs(df_sorted["ค่าใช้จ่าย"] - input_cost)
        nearest = df_sorted.nsmallest(5, "ต่างจากที่กรอก")

        st.write(f"**5 courses closest to {input_cost:,.0f} baht:**")
        st.table(nearest[["มหาวิทยาลัย", "คณะ", "ชื่อหลักสูตร", "ค่าใช้จ่าย"]])


# ---------------------- Add a Course search table page ----------------------
elif page == "Course search table":

    st.title("📋 Course search table")

    option_uni = st.multiselect("Select a university", sorted(df["มหาวิทยาลัย"].unique()))
    option_type = st.multiselect("Select course type", sorted(df["ประเภทหลักสูตร"].dropna().unique()))

    filtered_df = df.copy()

    if option_uni:
        filtered_df = filtered_df[filtered_df["มหาวิทยาลัย"].isin(option_uni)]
    if option_type:
        filtered_df = filtered_df[filtered_df["ประเภทหลักสูตร"].isin(option_type)]

    # st.dataframe(filtered_df, use_container_width=True)
    
        # Select the columns to sort as desired.
    columns_order = ["มหาวิทยาลัย", "คณะ", "วิทยาเขต", "ชื่อหลักสูตร", "ประเภทหลักสูตร", "ค่าใช้จ่าย"]
    df_show = filtered_df[columns_order]

    # Rename the table header (if the current name does not match)
    df_show = df_show.rename(columns={
        "มหาวิทยาลัย": "University",
        "คณะ": "Faculty",
        "วิทยาเขต": "Campus",
        "ชื่อหลักสูตร": "Course Name",
        "ประเภทหลักสูตร": "Course type",
        "ค่าใช้จ่าย": "Tuition Fees"
    })

    # show table
    st.table(df_show)