import streamlit as st
from CMGutils import clean_text
from CMGchain import Chain
from CMGportfolio import Portfolio
import os

st.title("Cold Email Generator")

# Load CSV and portfolio
csv_path = os.path.join(os.path.dirname(__file__), "Resource", "my_portfolio.csv")
portfolio = Portfolio(csv_path)
chain = Chain()

# Input job description
job_desc = st.text_area("Paste Job Description Here", height=300)

# Choose a project
options = [f"{p['Techstack']} — {p['Links']}" for p in portfolio.projects]
selected = st.selectbox("Select a project to include", options)

# Extract selected link
selected_link = portfolio.projects[options.index(selected)]['Links']

if st.button("Generate Cold Email"):
    cleaned = clean_text(job_desc)
    email = chain.write_email([cleaned], selected_link)
    st.subheader("📧 Generated Cold Email")
    st.write(email[0])
