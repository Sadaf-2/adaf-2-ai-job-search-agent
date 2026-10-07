import streamlit as st
import requests
import re
import html

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pakistan AI Job Search Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Pakistan AI Job Search Assistant")
st.write(
    "Find relevant technology jobs in Pakistan based on your skills."
)

# =========================================================
# PAKISTAN CITIES
# =========================================================

PAKISTAN_CITIES = {
    "All Pakistan": "Pakistan",
    "Islamabad": "Islamabad, Pakistan",
    "Rawalpindi": "Rawalpindi, Pakistan",
    "Lahore": "Lahore, Pakistan",
    "Karachi": "Karachi, Pakistan",
    "Peshawar": "Peshawar, Pakistan",
    "Faisalabad": "Faisalabad, Pakistan",
    "Multan": "Multan, Pakistan",
    "Quetta": "Quetta, Pakistan"
}

# =========================================================
# TECH KEYWORDS
# =========================================================

TECH_KEYWORDS = [
    "software",
    "developer",
    "frontend",
    "front-end",
    "backend",
    "back-end",
    "full stack",
    "full-stack",
    "web developer",
    "software engineer",
    "react",
    "javascript",
    "typescript",
    "python",
    "java",
    "php",
    "node",
    "node.js",
    "fastapi",
    "flask",
    "django",
    "angular",
    "vue",
    "next.js",
    "sql",
    "mongodb",
    "database",
    "api",
    "rest api",
    "devops",
    "cloud",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "qa",
    "quality assurance",
    "sqa",
    "tester",
    "automation testing",
    "ui/ux",
    "ui ux",
    "ux designer",
    "ui designer",
    "figma",
    "data analyst",
    "data scientist",
    "machine learning",
    "artificial intelligence",
    "ai engineer",
    "mobile developer",
    "android",
    "ios",
    "flutter",
    "react native",
    "cyber security",
    "cybersecurity"
]

# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "react.js", "reactjs"],
    "python": ["python"],
    "java": ["java"],
    "php": ["php"],
    "node": ["node", "node.js", "nodejs"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "git": ["git", "github", "gitlab"],
    "figma": ["figma"],
    "ui/ux": [
        "ui/ux",
        "ui ux",
        "user interface",
        "user experience"
    ],
    "api": [
        "api",
        "rest api",
        "restful api"
    ],
    "redux": ["redux"],
    "nextjs": ["next.js", "nextjs"],
    "tailwind": ["tailwind", "tailwind css"],
    "bootstrap": ["bootstrap"],
    "docker": ["docker"],
    "aws": ["aws"],
    "azure": ["azure"],
    "flutter": ["flutter"],
    "react native": ["react native"],
    "figma": ["figma"]
}

# =========================================================
# CLEAN DESCRIPTION
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = html.unescape(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# USER SKILLS
# =========================================================

def get_user_skills(skill_text):

    skills = []

    for skill in skill_text.split(","):

        skill = skill.strip().lower()

        if skill:
            skills.append(skill)

    return skills


# =========================================================
# CHECK IF TECH JOB
# =========================================================

def is_tech_job(title, description):

    text = (
        title
        + " "
        + description
    ).lower()

    for keyword in TECH_KEYWORDS:

        if keyword in text:
            return True

    return False


# =========================================================
# MATCH SKILLS
# =========================================================

def calculate_match(
    user_skills,
    job_title,
    job_description
):

    text = (
        job_title
        + " "
        + job_description
    ).lower()

    matched = []

    for skill in user_skills:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill]
        )

        found = False

        for alias in aliases:

            if alias.lower() in text:

                found = True
                break

        if found:
            matched.append(skill)

    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    if len(user_skills) == 0:

        score = 0

    else:

        score = int(
            (
                len(matched)
                /
                len(user_skills)
            )
            * 100
        )

    return score, matched


# =========================================================
# FIND MISSING COMMON SKILLS
# =========================================================

def find_missing_skills(
    user_skills,
    job_description
):

    text = job_description.lower()

    common_skills = [
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "python",
        "java",
        "php",
        "node",
        "fastapi",
        "flask",
        "django",
        "sql",
        "mongodb",
        "git",
        "github",
        "figma",
        "redux",
        "nextjs",
        "tailwind",
        "docker",
        "aws",
        "azure",
        "flutter",
        "react native"
    ]

    missing = []

    for skill in common_skills:

        if skill in user_skills:
            continue

        aliases = SKILL_ALIASES.get(
            skill,
            [skill]
        )

        found = False

        for alias in aliases:

            if alias.lower() in text:

                found = True
                break

        if found:

            missing.append(skill)

    return missing[:8]


# =========================================================
# GET JOBS FROM JSEARCH
# =========================================================

def get_jobs(
    query,
    location,
    api_key
):

    url = (
        "https://jsearch.p.rapidapi.com/search"
    )

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": f"{query} in {location}",
        "page": "1",
        "num_pages": "1",
        "country": "pk"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code != 200:

        raise Exception(
            f"API Error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    return data.get(
        "data",
        []
    )


# =========================================================
# API KEY
# =========================================================

try:

    RAPIDAPI_KEY = st.secrets[
        "RAPIDAPI_KEY"
    ]

except Exception:

    RAPIDAPI_KEY = ""

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Job Search Settings")

    st.write(
        "Pakistan Technology Jobs"
    )

    st.info(
        "Add your skills separated by commas."
    )

# =========================================================
# USER INPUT
# =========================================================

skills_input = st.text_input(
    "💻 Your Skills",
    placeholder=(
        "HTML, CSS, JavaScript, React"
    )
)

location_name = st.selectbox(
    "📍 Job Location",
    list(
        PAKISTAN_CITIES.keys()
    )
)

job_type = st.selectbox(
    "💼 Job Type",
    [
        "Any",
        "Full-time",
        "Part-time",
        "Internship",
        "Contract"
    ]
)

experience = st.selectbox(
    "🎓 Experience Level",
    [
        "Any",
        "Entry Level",
        "Junior",
        "Mid Level",
        "Senior"
    ]
)

number_of_jobs = st.slider(
    "🔢 Number of Jobs",
    5,
    30,
    15
)

# =========================================================
# SEARCH BUTTON
# =========================================================

if st.button(
    "🔍 Find Pakistan Tech Jobs",
    type="primary"
):

    if not RAPIDAPI_KEY:

        st.error(
            "RapidAPI key is missing. "
            "Add RAPIDAPI_KEY in Streamlit Secrets."
        )

        st.stop()

    if not skills_input:

        st.warning(
            "Please enter your skills first."
        )

        st.stop()

    user_skills = get_user_skills(
        skills_input
    )

    selected_location = PAKISTAN_CITIES[
        location_name
    ]

    # -----------------------------------------------------
    # SEARCH QUERY
    # -----------------------------------------------------

    search_query = " OR ".join(
        user_skills
    )

    with st.spinner(
        "🔎 Searching Pakistan tech jobs..."
    ):

        try:

            jobs = get_jobs(
                search_query,
                selected_location,
                RAPIDAPI_KEY
            )

        except Exception as e:

            st.error(
                f"Could not fetch jobs: {e}"
            )

            st.stop()

    # =====================================================
    # ANALYZE JOBS
    # =====================================================

    analyzed_jobs = []

    for job in jobs:

        title = job.get(
            "job_title",
            ""
        )

        company = job.get(
            "employer_name",
            "Unknown Company"
        )

        city = job.get(
            "job_city",
            ""
        )

        state = job.get(
            "job_state",
            ""
        )

        country = job.get(
            "job_country",
            "Pakistan"
        )

        description = clean_text(
            job.get(
                "job_description",
                ""
            )
        )

        employment = job.get(
            "job_employment_type",
            "Not specified"
        )

        apply_link = job.get(
            "job_apply_link",
            ""
        )

        # -------------------------------------------------
        # TECH FILTER
        # -------------------------------------------------

        if not is_tech_job(
            title,
            description
        ):

            continue

        # -------------------------------------------------
        # JOB TYPE FILTER
        # -------------------------------------------------

        if job_type != "Any":

            if job_type.lower() not in (
                employment.lower()
            ):

                continue

        # -------------------------------------------------
        # MATCH
        # -------------------------------------------------

        score, matched = calculate_match(
            user_skills,
            title,
            description
        )

        missing = find_missing_skills(
            user_skills,
            description
        )

        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        full_location = ", ".join(
            [
                x
                for x in [
                    city,
                    state,
                    country
                ]
                if x
            ]
        )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        analyzed_jobs.append(
            {
                "title": title,
                "company": company,
                "location": full_location,
                "description": description,
                "employment": employment,
                "apply_link": apply_link,
                "score": score,
                "matched": matched,
                "missing": missing
            }
        )

    # =====================================================
    # SORT
    # =====================================================

    analyzed_jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # =====================================================
    # RESULTS
    # =====================================================

    st.success(
        f"Found {len(analyzed_jobs)} relevant "
        f"Pakistan tech jobs."
    )

    if not analyzed_jobs:

        st.warning(
            "No relevant jobs found. "
            "Try broader skills such as "
            "JavaScript, Python, React or Software."
        )

        st.stop()

    # =====================================================
    # TOP MATCHES
    # =====================================================

    st.header(
        "🎯 Best Job Matches"
    )

    for job in analyzed_jobs[
        :number_of_jobs
    ]:

        score = job["score"]

        # -------------------------------------------------
        # MATCH LABEL
        # -------------------------------------------------

        if score >= 75:

            label = "🟢 Excellent Match"

        elif score >= 50:

            label = "🟡 Good Match"

        elif score >= 25:

            label = "🟠 Partial Match"

        else:

            label = "🔴 Low Match"

        # -------------------------------------------------
        # JOB CARD
        # -------------------------------------------------

        with st.container():

            st.subheader(
                job["title"]
            )

            st.write(
                f"🏢 **Company:** "
                f"{job['company']}"
            )

            st.write(
                f"📍 **Location:** "
                f"{job['location']}"
            )

            st.write(
                f"💼 **Employment:** "
                f"{job['employment']}"
            )

            st.markdown(
                f"## {label} — {score}%"
            )

            # ------------------------------------------------
            # MATCHED
            # ------------------------------------------------

            if job["matched"]:

                st.write(
                    "✅ **Your matching skills:** "
                    + ", ".join(
                        job["matched"]
                    )
                )

            # ------------------------------------------------
            # MISSING
            # ------------------------------------------------

            if job["missing"]:

                st.write(
                    "📚 **Skills you may need:** "
                    + ", ".join(
                        job["missing"]
                    )
                )

                st.info(
                    "💡 Learn these skills to "
                    "increase your chances for "
                    "this type of job."
                )

            else:

                st.success(
                    "🔥 Your listed skills match "
                    "the job requirements well."
                )

            # ------------------------------------------------
            # DESCRIPTION
            # ------------------------------------------------

            if job["description"]:

                with st.expander(
                    "📄 Job Description"
                ):

                    st.write(
                        job["description"]
                    )

            # ------------------------------------------------
            # APPLY
            # ------------------------------------------------

            if job["apply_link"]:

                st.link_button(
                    "🚀 Apply for Job",
                    job["apply_link"]
                )

            st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "💼 Pakistan AI Job Search Assistant | "
    "Skills-based job matching"
)
