import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aptamer Database", layout="wide")
st.title("Aptamer Database")
st.caption("Structured aptamer data extracted from PubMed literature using Gemini 2.5 Flash.")

df = pd.read_excel("part2_gemini/results.xlsx")

col1, col2 = st.columns(2)
with col1:
    search = st.text_input("Search by aptamer name or sequence")
with col2:
    pool_filter = st.multiselect("Pool type", options=sorted(df["pool_type"].dropna().unique()))

filtered = df.copy()
if search:
    mask = (
        filtered["aptamer_name"].str.contains(search, case=False, na=False) |
        filtered["sequence"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if pool_filter:
    filtered = filtered[filtered["pool_type"].isin(pool_filter)]

st.dataframe(filtered, use_container_width=True, hide_index=True)
st.caption(f"{len(filtered)} of {len(df)} records shown")
