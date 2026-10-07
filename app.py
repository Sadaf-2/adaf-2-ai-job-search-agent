import streamlit as st
import requests
import re
import html

st.set_page_config(
    page_title="AI Job Search Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Search Assistant")
st.write("Find relevant jobs based on your skills and discover what you need to learn.")


# -----------------------------
# USER INPUT
# -----------------------------

skills_input = st.text_input(
    "💻 Your Skills",
    placeholder="e.g. HTML, CSS, JavaScript, React"
)

location = st.selectbox(
    "📍 Preferred Location",
    [
        "Islamabad",
        "Rawalpindi",
        "Islamabad + Rawalpindi",
        "Remote",
        "Any Location"
    ]
)

job_type = st.selectbox(
    "💼 Job Type",
    [
        "All",
        "Full-Time",
        "Part-Time",
        "Internship"
    ]
)


# -----------------------------
# SKILL ALIASES
# -----------------------------

skill_aliases = {
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "react.js", "reactjs"],
    "python": ["python"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "node": ["node", "node.js", "nodejs"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "git": ["git", "github", "gitlab"],
    "figma": ["figma"],
    "ui/ux": ["ui/ux", "ui ux", "user interface", "user experience"],
    "api": ["api", "rest api", "restful api"],
    "redux": ["redux"],
    "nextjs": ["next.js", "nextjs"],
    "mongodb": ["mongodb", "mongo"],
}


# -----------------------------
# CLEAN HTML
# -----------------------------

def clean_text(text):

    text = re.sub("<.*?>", " ", text)

    text = html.unescape(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# GET USER SKILLS
# -----------------------------

def get_user_skills():

    skills = []

    for skill in skills_input.split(","):

        skill = skill.strip().lower()

        if skill:
            skills.append(skill)

    return skills


# -----------------------------
# FIND MATCHING SKILLS
# -----------------------------

def calculate_match(user_skills, job_text):

    matched = []
    missing = []

    job_text = job_text.lower()

    for skill in user_skills:

        aliases = skill_aliases.get(
            skill,
            [skill]
        )

        found = False

        for alias in aliases:

            if alias.lower() in job_text:

                found = True
                break

        if found:
            matched.append(skill)

        else:
            missing.append(skill)

    if len(user_skills) == 0:
        score = 0

    else:
        score = int(
            (len(matched) / len(user_skills)) * 100
        )

    return score, matched, missing


# -----------------------------
# GET JOBS
# -----------------------------

def get_jobs():

    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    return response.json().get(
        "jobs",
        []
    )


# -----------------------------
# SEARCH BUTTON
# -----------------------------

if st.button("🔍 Find Relevant Jobs"):

    if not skills_input:

        st.warning(
            "Please enter your skills first."
        )

    else:

        user_skills = get_user_skills()

        with st.spinner(
            "Searching and analyzing jobs..."
        ):

            try:

                jobs = get_jobs()

                analyzed_jobs = []

                for job in jobs:

                    title = job.get(
                        "title",
                        ""
                    )

                    company = job.get(
                        "company_name",
                        "Unknown"
                    )

                    job_location = job.get(
                        "candidate_required_location",
                        "Remote"
                    )

                    description = clean_text(
                        job.get(
                            "description",
                            ""
                        )
                    )

                    category = job.get(
                        "category",
                        ""
                    )

                    job_type_api = job.get(
                        "job_type",
                        ""
                    )

                    combined_text = (
                        title
                        + " "
                        + description
                        + " "
                        + category
                    )

                    # -----------------------------
                    # LOCATION FILTER
                    # -----------------------------

                    if location == "Remote":

                        if "remote" not in job_location.lower():

                            continue

                    elif location == "Islamabad":

                        if "islamabad" not in (
                            job_location.lower()
                        ):

                            continue

                    elif location == "Rawalpindi":

                        if "rawalpindi" not in (
                            job_location.lower()
                        ):

                            continue

                    elif location == "Islamabad + Rawalpindi":

                        location_text = (
                            job_location.lower()
                        )

                        if (
                            "islamabad" not in location_text
                            and
                            "rawalpindi" not in location_text
                            and
                            "remote" not in location_text
                        ):

                            continue

                    # Any Location = no location filtering

                    # -----------------------------
                    # JOB TYPE FILTER
                    # -----------------------------

                    if job_type != "All":

                        if job_type.lower() not in (
                            job_type_api.lower()
                        ):

                            continue

                    # -----------------------------
                    # MATCH SCORE
                    # -----------------------------

                    score, matched, missing = calculate_match(
                        user_skills,
                        combined_text
                    )

                    job["match_score"] = score
                    job["matched_skills"] = matched
                    job["missing_skills"] = missing

                    analyzed_jobs.append(job)

                # -----------------------------
                # SORT BY MATCH
                # -----------------------------

                analyzed_jobs.sort(
                    key=lambda x: x["match_score"],
                    reverse=True
                )

                # -----------------------------
                # RESULTS
                # -----------------------------

                if not analyzed_jobs:

                    st.warning(
                        "No jobs found for these filters."
                    )

                else:

                    st.success(
                        f"Found {len(analyzed_jobs)} jobs."
                    )

                    # -----------------------------
                    # RELEVANT JOBS
                    # -----------------------------

                    st.header(
                        "🎯 Recommended Jobs"
                    )

                    relevant_jobs = [
                        job
                        for job in analyzed_jobs
                        if job["match_score"] >= 30
                    ]

                    if not relevant_jobs:

                        st.info(
                            "No highly relevant jobs found. "
                            "Try adding more skills."
                        )

                    for job in relevant_jobs[:15]:

                        score = job[
                            "match_score"
                        ]

                        if score >= 75:

                            badge = "🟢 Strong Match"

                        elif score >= 50:

                            badge = "🟡 Good Match"

                        else:

                            badge = "🟠 Partial Match"

                        with st.container():

                            st.subheader(
                                job.get(
                                    "title",
                                    "Job"
                                )
                            )

                            st.write(
                                f"🏢 **Company:** "
                                f"{job.get('company_name', 'Unknown')}"
                            )

                            st.write(
                                f"📍 **Location:** "
                                f"{job.get('candidate_required_location', 'Remote')}"
                            )

                            st.write(
                                f"💼 **Type:** "
                                f"{job.get('job_type', 'Unknown')}"
                            )

                            st.markdown(
                                f"### {badge} — {score}%"
                            )

                            # -------------------------
                            # MATCHED SKILLS
                            # -------------------------

                            if job[
                                "matched_skills"
                            ]:

                                st.write(
                                    "✅ **Your matching skills:** "
                                    + ", ".join(
                                        job[
                                            "matched_skills"
                                        ]
                                    )
                                )

                            # -------------------------
                            # MISSING SKILLS
                            # -------------------------

                            if job[
                                "missing_skills"
                            ]:

                                st.write(
                                    "📚 **Skills to improve:** "
                                    + ", ".join(
                                        job[
                                            "missing_skills"
                                        ]
                                    )
                                )

                                st.info(
                                    "💡 Recommendation: "
                                    "Learn the missing skills "
                                    "before or alongside applying."
                                )

                            else:

                                st.success(
                                    "🔥 Your listed skills match "
                                    "the requirements well. "
                                    "Consider applying!"
                                )

                            description = job.get(
                                "description",
                                ""
                            )

                            st.write(
                                description[:700]
                                + "..."
                            )

                            st.link_button(
                                "🚀 Apply for Job",
                                job.get(
                                    "url",
                                    "#"
                                )
                            )

                            st.divider()

                    # -----------------------------
                    # ALL JOBS
                    # -----------------------------

                    with st.expander(
                        "📋 Show All Jobs"
                    ):

                        for job in analyzed_jobs:

                            st.write(
                                f"**{job.get('title', 'Job')}**"
                            )

                            st.write(
                                f"🏢 {job.get('company_name', 'Unknown')}"
                            )

                            st.write(
                                f"📍 {job.get('candidate_required_location', 'Remote')}"
                            )

                            st.write(
                                f"🎯 Match: "
                                f"{job['match_score']}%"
                            )

                            st.link_button(
                                "Apply",
                                job.get(
                                    "url",
                                    "#"
                                )
                            )

                            st.divider()

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )
