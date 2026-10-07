import streamlit as st
import requests

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
    placeholder="e.g. Rawalpindi, Islamabad, Remote"
)

job_type = st.selectbox(
    "Job Type",
    ["Internship", "Full-Time", "Part-Time", "Remote"]
)

if st.button("🔍 Find Jobs"):

    if not skills:
        st.warning("Please enter your skills.")
    else:

        st.info("Searching for jobs...")

        try:
            url = "https://remotive.com/api/remote-jobs"

            response = requests.get(url, timeout=15)

            if response.status_code == 200:

                data = response.json()
                jobs = data.get("jobs", [])

                st.success(f"Found {len(jobs)} jobs!")

                # Show first 10 jobs
                for job in jobs[:10]:

                    st.subheader(job.get("title", "No title"))

                    st.write(
                        f"🏢 **Company:** {job.get('company_name', 'Unknown')}"
                    )

                    st.write(
                        f"📍 **Location:** {job.get('candidate_required_location', 'Remote')}"
                    )

                    st.write(
                        f"📅 **Type:** {job.get('job_type', 'Unknown')}"
                    )

                    description = job.get("description", "")

                    # Remove HTML from description
                    import re

                    clean_description = re.sub(
                        "<.*?>",
                        "",
                        description
                    )

                    st.write(clean_description[:500] + "...")

                    st.link_button(
                        "Apply for this job",
                        job.get("url", "#")
                    )

                    st.divider()

            else:
                st.error("Could not fetch jobs.")

        except Exception as e:
            st.error(f"Error: {e}")
