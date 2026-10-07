import streamlit as st
import requests
import re
import html


# =========================================================
# PAGE
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
# LOCATIONS
# =========================================================

PAKISTAN_CITIES = {
    "All Pakistan": "",
    "Islamabad": "Islamabad",
    "Rawalpindi": "Rawalpindi",
    "Lahore": "Lahore",
    "Karachi": "Karachi",
    "Peshawar": "Peshawar",
    "Faisalabad": "Faisalabad",
    "Multan": "Multan",
    "Quetta": "Quetta"
}


# =========================================================
# TECH KEYWORDS
# =========================================================

TECH_KEYWORDS = [
    "developer",
    "software",
    "frontend",
    "front-end",
    "backend",
    "back-end",
    "full stack",
    "full-stack",
    "web",
    "engineer",
    "react",
    "javascript",
    "typescript",
    "python",
    "java",
    "php",
    "node",
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
    "devops",
    "cloud",
    "aws",
    "azure",
    "docker",
    "qa",
    "quality assurance",
    "sqa",
    "tester",
    "testing",
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
    "react native"
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
    "tailwind": [
        "tailwind",
        "tailwind css"
    ],
    "bootstrap": ["bootstrap"],
    "docker": ["docker"],
    "aws": ["aws"],
    "azure": ["azure"],
    "flutter": ["flutter"],
    "react native": ["react native"]
}


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(value):

    if value is None:
        return ""

    text = str(value)

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

        if skill and skill not in skills:
            skills.append(skill)

    return skills


# =========================================================
# TECH JOB
# =========================================================

def is_tech_job(title, description):

    text = (
        clean_text(title)
        + " "
        + clean_text(description)
    ).lower()

    return any(
        keyword in text
        for keyword in TECH_KEYWORDS
    )


# =========================================================
# MATCH SCORE
# =========================================================

def calculate_match(
    user_skills,
    title,
    description
):

    text = (
        clean_text(title)
        + " "
        + clean_text(description)
    ).lower()

    matched = []

    for skill in user_skills:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill]
        )

        for alias in aliases:

            if alias.lower() in text:

                matched.append(skill)
                break

    if not user_skills:
        return 0, []

    score = int(
        len(matched)
        / len(user_skills)
        * 100
    )

    return score, matched


# =========================================================
# MISSING SKILLS
# =========================================================

def find_missing_skills(
    user_skills,
    description
):

    text = clean_text(
        description
    ).lower()

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

        for alias in aliases:

            if alias.lower() in text:

                missing.append(skill)
                break

    return missing[:8]


# =========================================================
# JSEARCH
# =========================================================

def get_jobs(
    skills,
    location,
    api_key,
    job_type
):

    url = (
        "https://jsearch.p.rapidapi.com/"
        "search-v2"
    )

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host":
            "jsearch.p.rapidapi.com"
    }

    # -----------------------------------------------------
    # USE ACTUAL USER SKILLS IN SEARCH
    # -----------------------------------------------------

    if skills:

        skill_query = " ".join(
            skills[:5]
        )

    else:

        skill_query = "software developer"


    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    if location:

        query = (
            f"{skill_query} jobs "
            f"in {location} Pakistan"
        )

    else:

        query = (
            f"{skill_query} jobs "
            f"in Pakistan"
        )


    params = {
        "query": query,
        "num_pages": "1",
        "country": "pk",
        "language": "en",
        "date_posted": "month"
    }


    # -----------------------------------------------------
    # JOB TYPE
    # -----------------------------------------------------

    if job_type == "Full-time":

        params["employment_types"] = "FULLTIME"

    elif job_type == "Part-time":

        params["employment_types"] = "PARTTIME"

    elif job_type == "Internship":

        params["employment_types"] = "INTERN"

    elif job_type == "Contract":

        params["employment_types"] = "CONTRACTOR"


    # -----------------------------------------------------
    # REQUEST
    # -----------------------------------------------------

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )


    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    if response.status_code != 200:

        raise Exception(
            f"API Error "
            f"{response.status_code}: "
            f"{response.text}"
        )


    # -----------------------------------------------------
    # JSON
    # -----------------------------------------------------

    try:

        result = response.json()

    except Exception:

        raise Exception(
            "JSearch returned invalid JSON."
        )


    # -----------------------------------------------------
    # DATA
    # -----------------------------------------------------

    if not isinstance(result, dict):

        return []


    data = result.get(
        "data",
        []
    )


    if isinstance(data, list):

        return data


    return []


# =========================================================
# RAPIDAPI SECRET
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

    st.header(
        "⚙️ Search Settings"
    )

    st.write(
        "🇵🇰 Pakistan Technology Jobs"
    )

    st.info(
        "Enter your skills separated "
        "by commas."
    )


# =========================================================
# INPUTS
# =========================================================

skills_input = st.text_input(
    "💻 Your Skills",
    placeholder="HTML, CSS, JavaScript, React"
)


location_name = st.selectbox(
    "📍 Job Location",
    list(PAKISTAN_CITIES.keys())
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
            "Add RAPIDAPI_KEY in "
            "Streamlit Secrets."
        )

        st.stop()


    if not skills_input.strip():

        st.warning(
            "Please enter your skills first."
        )

        st.stop()


    user_skills = get_user_skills(
        skills_input
    )


    selected_location = (
        PAKISTAN_CITIES[
            location_name
        ]
    )


    # =====================================================
    # FETCH JOBS
    # =====================================================

    with st.spinner(
        "🔎 Searching Pakistan jobs..."
    ):

        try:

            jobs = get_jobs(
                user_skills,
                selected_location,
                RAPIDAPI_KEY,
                job_type
            )

        except Exception as e:

            st.error(
                f"Could not fetch jobs: {e}"
            )

            st.stop()


    # =====================================================
    # NO API RESULTS
    # =====================================================

    if not jobs:

        st.warning(
            "JSearch returned no jobs "
            "for this search."
        )

        st.info(
            "Try a broader skill such as "
            "JavaScript, Python, React "
            "or Software Developer."
        )

        st.stop()


    # =====================================================
    # ANALYZE
    # =====================================================

    analyzed_jobs = []


    for job in jobs:

        if not isinstance(
            job,
            dict
        ):
            continue


        title = clean_text(
            job.get(
                "job_title",
                ""
            )
        )


        company = clean_text(
            job.get(
                "employer_name",
                "Unknown Company"
            )
        )


        city = clean_text(
            job.get(
                "job_city",
                ""
            )
        )


        state = clean_text(
            job.get(
                "job_state",
                ""
            )
        )


        country = clean_text(
            job.get(
                "job_country",
                "Pakistan"
            )
        )


        description = clean_text(
            job.get(
                "job_description",
                ""
            )
        )


        employment = clean_text(
            job.get(
                "job_employment_type",
                "Not specified"
            )
        )


        apply_link = clean_text(
            job.get(
                "job_apply_link",
                ""
            )
        )


        if not title:
            continue


        # -------------------------------------------------
        # TECH FILTER
        # -------------------------------------------------

        if not is_tech_job(
            title,
            description
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


        # -------------------------------------------------
        # MISSING
        # -------------------------------------------------

        missing = find_missing_skills(
            user_skills,
            description
        )


        # -------------------------------------------------
        # LOCATION
        # -------------------------------------------------

        location_parts = []

        if city:
            location_parts.append(city)

        if state:
            location_parts.append(state)

        if country:
            location_parts.append(country)


        full_location = ", ".join(
            location_parts
        )


        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        job_text = (
            title
            + " "
            + description
        ).lower()


        if experience == "Entry Level":

            keywords = [
                "entry level",
                "entry-level",
                "no experience",
                "fresh graduate",
                "junior",
                "0-1 years",
                "0-2 years"
            ]

            if not any(
                x in job_text
                for x in keywords
            ):
                continue


        elif experience == "Junior":

            keywords = [
                "junior",
                "entry level",
                "entry-level",
                "fresh graduate",
                "0-2 years",
                "1-2 years"
            ]

            if not any(
                x in job_text
                for x in keywords
            ):
                continue


        elif experience == "Mid Level":

            keywords = [
                "mid level",
                "mid-level",
                "2-5 years",
                "3-5 years"
            ]

            if not any(
                x in job_text
                for x in keywords
            ):
                continue


        elif experience == "Senior":

            keywords = [
                "senior",
                "lead",
                "manager",
                "5+ years",
                "5 years"
            ]

            if not any(
                x in job_text
                for x in keywords
            ):
                continue


        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        analyzed_jobs.append({

            "title": title,

            "company": company,

            "location": full_location,

            "description": description,

            "employment": employment,

            "apply_link": apply_link,

            "score": score,

            "matched": matched,

            "missing": missing

        })


    # =====================================================
    # SORT
    # =====================================================

    analyzed_jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # =====================================================
    # RESULT
    # =====================================================

    st.success(
        f"Found {len(analyzed_jobs)} "
        f"relevant jobs."
    )


    if not analyzed_jobs:

        st.warning(
            "Jobs were returned, but "
            "none passed our technology "
            "filter."
        )

        st.info(
            "Try HTML, CSS, JavaScript, "
            "React or Python."
        )

        st.stop()


    # =====================================================
    # DISPLAY
    # =====================================================

    st.header(
        "🎯 Best Job Matches"
    )


    for job in analyzed_jobs[
        :number_of_jobs
    ]:

        score = job["score"]


        if score >= 75:

            label = "🟢 Excellent Match"

        elif score >= 50:

            label = "🟡 Good Match"

        elif score >= 25:

            label = "🟠 Partial Match"

        else:

            label = "🔴 Low Match"


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
                f"### {label} — {score}%"
            )


            if job["matched"]:

                st.write(
                    "✅ **Matching skills:** "
                    + ", ".join(
                        job["matched"]
                    )
                )


            if job["missing"]:

                st.write(
                    "📚 **Skills to learn:** "
                    + ", ".join(
                        job["missing"]
                    )
                )

                st.info(
                    "💡 Learning these skills "
                    "can improve your chances "
                    "for similar jobs."
                )

            else:

                st.success(
                    "🔥 Your listed skills "
                    "match this job well."
                )


            if job["description"]:

                with st.expander(
                    "📄 Job Description"
                ):

                    st.write(
                        job["description"]
                    )


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
    "💼 Pakistan AI Job Search Assistant "
    "| JSearch + Skills Matching"
)
