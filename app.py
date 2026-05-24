import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Dashboard -  Consumer Complaints", layout="wide")

#connect database
@st.cache_resource
def get_con():
    return duckdb.connect("complaints.duckdb")

con = get_con()
total = con.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
st.write(f"Tổng số khiếu nại: {total:,}")