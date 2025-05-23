import streamlit as st
import requests

st.set_page_config(page_title="EdgeStack MVP", layout="centered")
st.title("🏈 Welcome to EdgeStack")
st.write("Fantasy Start/Sit and Prop Betting Insights")

# Test call to FastAPI
try:
    res = requests.get("http://localhost:8000/")
    st.success(f"API says: {res.json()['message']}")
except:
    st.error("⚠️ Cannot reach FastAPI backend.")