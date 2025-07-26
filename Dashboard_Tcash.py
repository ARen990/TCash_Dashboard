import streamlit as st
import pandas as pd
import json

# Load data
with open("D:\Y3\J.bod\data\data_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["ค่าใช้จ่าย"] = pd.to_numeric(df["ค่าใช้จ่าย"], errors="coerce")

st.set_page_config(page_title="University Course Dashboard", layout="wide")
# st.title("🎓 University Course Dashboard")

page = st.sidebar.selectbox(
    "MENU",
    ["Dashboard", "Find Tuition Fees", "Course search table"]
)

# ---------------------- เพิ่มหน้า Dashboard ----------------------
if page == "Dashboard":

    st.title("📊 Dashboard")

# ---------------------- เพิ่มหน้า Dashboard ----------------------
elif page == "Find Tuition Fees":

    st.title("🔍 Find some tuition fees")

# ---------------------- หน้า Course search table ----------------------
elif page == "Course search table":

    st.title("📋 Course search table")