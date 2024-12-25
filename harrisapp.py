import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Tennis Rankings Explorer", layout="wide")
st.title("🎾 Tennis Rankings Explorer")

st.sidebar.header("Filters")

current_year = datetime.now().year
current_week = datetime.now().isocalendar()[1]
year = st.sidebar.number_input("Year", min_value=2000, max_value=current_year, value=current_year)
week = st.sidebar.number_input("Week", min_value=1, max_value=53, value=current_week)

gender = st.sidebar.selectbox("Gender", ["men", "women"])
rank_range = st.sidebar.slider("Rank Range", min_value=1, max_value=100, value=(1, 10))
search_competitor = st.sidebar.text_input("Search Competitors")

api_key = "J3BFeVNDnNOR12ENMO9xnQVHRzGLsxPJDn7OMRPl"  

competitions_url = f"https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key={api_key}&year={year}&week={week}"
headers = {"accept": "application/json"}

st.sidebar.header("Fetch Competitions Data")
st.sidebar.write(f"Fetching competition data for Year: {year}, Week: {week}...")

try:
    competitions_response = requests.get(competitions_url, headers=headers)
    if competitions_response.status_code == 200:
        competitions_data = competitions_response.json().get("competitions", [])
        st.sidebar.success("Competitions data fetched successfully!")
    else:
        competitions_data = []
        st.sidebar.error(f"Failed to fetch competitions data. Status code: {competitions_response.status_code}")
except Exception as e:
    competitions_data = []
    st.sidebar.error(f"Error: {str(e)}")

complexes_url = f"https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key={api_key}"

st.sidebar.header("Fetch Venues and Complexes Data")
st.sidebar.write("Fetching venues and complexes data...")

try:
    complexes_response = requests.get(complexes_url, headers=headers)
    if complexes_response.status_code == 200:
        complexes_data = complexes_response.json().get("complexes", [])
        st.sidebar.success("Venues and complexes data fetched successfully!")
    else:
        complexes_data = []
        st.sidebar.error(f"Failed to fetch venues data. Status code: {complexes_response.status_code}")
except Exception as e:
    complexes_data = []
    st.sidebar.error(f"Error: {str(e)}")

st.header("Competitions")
if competitions_data:
    competitions_df = pd.DataFrame(competitions_data)
    if not competitions_df.empty:
        st.dataframe(competitions_df)
    else:
        st.warning("No competition data available.")
else:
    st.warning("No competitions data available.")

st.header("Venues and Complexes")
if complexes_data:
    complexes_df = pd.DataFrame(complexes_data)
    if not complexes_df.empty:
        st.dataframe(complexes_df)
    else:
        st.warning("No venues data available.")
else:
    st.warning("No venues and complexes data available.")

rankings_data = {
    "Rank": range(1, 101),
    "Name": [f"Player {i}" for i in range(1, 101)],
    "Country": ["Country A", "Country B"] * 50,
    "Points": [1000 - i * 10 for i in range(100)],
    "Gender": ["men" if i % 2 == 0 else "women" for i in range(100)],
}
df = pd.DataFrame(rankings_data)

filtered_df = df[
    (df["Rank"] >= rank_range[0])
    & (df["Rank"] <= rank_range[1])
    & (df["Gender"] == gender)
]

if search_competitor:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_competitor, case=False)]

st.header("Rankings")
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    st.dataframe(filtered_df)
