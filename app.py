import streamlit as st

st.set_page_config(
    page_title="AI Job Search Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Search Assistant")
st.write("Find jobs that match your skills with AI.")

skills = st.text_input(
    "Enter your skills",
    placeholder="e.g. React, JavaScript, Python, UI/UX"
)

location = st.text_input(
    "Preferred location",
    placeholder="e.g. Remote, Islamabad, Rawalpindi"
)

job_type = st.selectbox(
    "Job Type",
    ["Internship", "Full-Time", "Part-Time", "Remote"]
)

if st.button("🔍 Find Jobs"):
    if skills and location:
        st.success("Job search started!")
        st.write("Skills:", skills)
        st.write("Location:", location)
        st.write("Job Type:", job_type)
    else:
        st.warning("Please enter your skills and preferred location.")
