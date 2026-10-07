
import streamlit as st
import requests
import re
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="JobPilot AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1120;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263244;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 28px;
    }

    .hero-box {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 25px;
    }

    .hero-small {
        color: #818cf8;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .hero-heading {
        color: #f8fafc;
        font-size: 34px;
        font-weight: 800;
        margin-top: 8px;
    }

    .hero-text {
        color: #94a3b8;
        font-size: 15px;
        line-height: 1.6;
    }

    .stat-box {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 15px;
        padding: 18px;
        text-align: center;
    }

    .stat-value {
        color: #818cf8;
        font-size: 28px;
        font-weight: 800;
    }

    .stat-label {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
    }

    .job-box {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 22px;
        margin-top: 16px;
        margin-bottom: 16px;
    }

    .job-title {
        color: #f8fafc;
        font-size: 20px;
        font-weight: 700;
    }

    .job-company {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 4px;
    }

    .match-score {
        color: #818cf8;
        font-size: 28px;
        font-weight: 800;
        text-align: center;
    }

    .match-text {
        color: #94a3b8;
        font-size: 12px;
        text-align: center;
    }

    .section-title {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 750;
        margin-top: 28px;
        margin-bottom: 10px;
    }

    .skill-title {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 7px;
        letter-spacing: 0.5px;
    }

    .skill {
        display: inline-block;
        background: #172554;
        border: 1px solid #3730a3;
        color: #c7d2fe;
        padding: 5px 9px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 5px;
        margin-bottom: 5px;
    }

    .missing {
        display: inline-block;
        background: #3f1722;
        border: 1px solid #7f1d1d;
        color: #fda4af;
        padding: 5px 9px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 5px;
        margin-bottom: 5px;
    }

    .footer {
        color: #64748b;
        text-align: center;
        margin-top: 45px;
        padding: 20px;
        border-top: 1px solid #1e293b;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATA
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
    "Quetta": "Quetta",
    "Abbottabad": "Abbottabad"
}


SKILL_ALIASES = {

    "html": ["html", "html5"],

    "css": ["css", "css3"],

    "javascript": [
        "javascript",
        "javascript",
        "ecmascript"
    ],

    "typescript": [
        "typescript",
        "typescript"
    ],

    "react": [
        "react",
        "react.js",
        "reactjs"
    ],

    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "php": [
        "php"
    ],

    "node": [
        "node",
        "node.js",
        "nodejs"
    ],

    "fastapi": [
        "fastapi"
    ],

    "flask": [
        "flask"
    ],

    "django": [
        "django"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "mongodb": [
        "mongodb",
        "mongo"
    ],

    "git": [
        "git",
        "github",
        "gitlab"
    ],

    "figma": [
        "figma"
    ],

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

    "redux": [
        "redux"
    ],

    "nextjs": [
        "next.js",
        "nextjs"
    ],

    "tailwind": [
        "tailwind",
        "tailwind css"
    ],

    "bootstrap": [
        "bootstrap"
    ],

    "docker": [
        "docker"
    ],

    "aws": [
        "aws"
    ],

    "azure": [
        "azure"
    ],

    "flutter": [
        "flutter"
    ],

    "react native": [
        "react native"
    ]
}


ROLE_ALIASES = {
    "web developer": [
        "web developer",
        "web development",
        "frontend developer",
        "front end developer",
        "full stack developer",
        "full-stack developer"
    ],

    "frontend developer": [
        "frontend developer",
        "front end developer",
        "front-end developer",
        "frontend engineer"
    ],

    "backend developer": [
        "backend developer",
        "back end developer",
        "back-end developer"
    ],

    "software developer": [
        "software developer",
        "software engineer"
    ],

    "full stack developer": [
        "full stack developer",
        "full-stack developer"
    ],

    "ui/ux designer": [
        "ui/ux designer",
        "ui ux designer",
        "ux designer",
        "ui designer"
    ]
}


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
# FUNCTIONS
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


def get_user_skills(text):

    skills = []

    for item in text.split(","):

        item = item.strip().lower()

        if not item:
            continue

        if item in ROLE_ALIASES:

            continue

        if item not in skills:

            skills.append(item)

    return skills


def get_user_roles(text):

    roles = []

    for item in text.split(","):

        item = item.strip().lower()

        if item in ROLE_ALIASES:

            roles.append(item)

    return roles


def is_tech_job(title, description):

    text = (
        title
        + " "
        + description
    ).lower()

    return any(
        keyword in text
        for keyword in TECH_KEYWORDS
    )


def calculate_match(
    user_skills,
    user_roles,
    title,
    description
):

    text = (
        clean_text(title)
        + " "
        + clean_text(description)
    ).lower()

    matched_skills = []

    for skill in user_skills:

        aliases = SKILL_ALIASES.get(
            skill,
            [skill]
        )

        for alias in aliases:

            if alias.lower() in text:

                matched_skills.append(
                    skill
                )

                break


    matched_roles = []

    for role in user_roles:

        aliases = ROLE_ALIASES.get(
            role,
            [role]
        )

        for alias in aliases:

            if alias.lower() in text:

                matched_roles.append(
                    role
                )

                break


    total_items = (
        len(user_skills)
        + len(user_roles)
    )


    matched_items = (
        len(matched_skills)
        + len(matched_roles)
    )


    if total_items == 0:

        return 0, [], []


    score = int(
        matched_items
        / total_items
        * 100
    )


    return (
        score,
        matched_skills,
        matched_roles
    )


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

                missing.append(
                    skill
                )

                break

    return missing[:8]


def get_jobs(
    search_text,
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


    if location:

        query = (
            f"{search_text} jobs "
            f"in {location} Pakistan"
        )

    else:

        query = (
            f"{search_text} jobs "
            f"in Pakistan"
        )


    params = {

        "query": query,

        "num_pages": "1",

        "country": "pk",

        "language": "en",

        "date_posted": "all"
    }


    if job_type == "Full-time":

        params[
            "employment_types"
        ] = "FULLTIME"


    elif job_type == "Part-time":

        params[
            "employment_types"
        ] = "PARTTIME"


    elif job_type == "Internship":

        params[
            "employment_types"
        ] = "INTERN"


    elif job_type == "Contract":

        params[
            "employment_types"
        ] = "CONTRACTOR"


    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )


    if response.status_code != 200:

        raise Exception(
            f"API Error "
            f"{response.status_code}: "
            f"{response.text}"
        )


    result = response.json()

    data = result.get(
        "data",
        []
    )


    if isinstance(
        data,
        list
    ):

        return data


    if isinstance(
        data,
        dict
    ):

        jobs = data.get(
            "jobs",
            []
        )

        if isinstance(
            jobs,
            list
        ):

            return jobs


    return []


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

    st.markdown(
        "## 💼 JobPilot AI"
    )

    st.caption(
        "Smart job discovery for Pakistan"
    )

    st.divider()

    st.markdown(
        "### ⚙️ Search Filters"
    )

    location_name = st.selectbox(
        "📍 Location",
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
        "🎓 Experience",
        [
            "Any",
            "Entry Level",
            "Junior",
            "Mid Level",
            "Senior"
        ]
    )

    number_of_jobs = st.slider(
        "🔢 Results",
        5,
        30,
        10
    )

    st.divider()

    st.markdown(
        """
        **How it works**

        1. Enter your skills
        2. Select a location
        3. Search live jobs
        4. Compare your skills
        5. Find missing skills
        6. Apply directly
        """
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="hero-box">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-small">'
    '✨ AI-POWERED CAREER ASSISTANT'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-heading">'
    'Find your next opportunity.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-text">'
    'Search technology jobs across Pakistan, '
    'compare your skills with real job requirements, '
    'discover what you should learn next, and apply faster.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SEARCH
# =========================================================

st.markdown(
    "### 🔎 Search Jobs"
)

skills_input = st.text_input(
    "Skills or job role",
    placeholder=(
        "Example: HTML, CSS, JavaScript, React"
    )
)

st.caption(
    "Tip: You can enter a job role too, e.g. "
    "Web Developer or Frontend Developer."
)


search_clicked = st.button(
    "🚀 Find My Best Jobs",
    type="primary",
    use_container_width=True
)


# =========================================================
# SEARCH ACTION
# =========================================================

if search_clicked:

    if not RAPIDAPI_KEY:

        st.error(
            "RapidAPI key is missing. "
            "Add RAPIDAPI_KEY in Streamlit Secrets."
        )

        st.stop()


    if not skills_input.strip():

        st.warning(
            "Please enter your skills or job role."
        )

        st.stop()


    user_skills = get_user_skills(
        skills_input
    )

    user_roles = get_user_roles(
        skills_input
    )


    # If no recognized role,
    # use the whole input as API query

    search_text = skills_input.strip()


    selected_location = (
        PAKISTAN_CITIES[
            location_name
        ]
    )


    with st.spinner(
        "🔎 Finding jobs for you..."
    ):

        try:

            jobs = get_jobs(
                search_text,
                selected_location,
                RAPIDAPI_KEY,
                job_type
            )

        except Exception as e:

            st.error(
                f"Could not fetch jobs: {e}"
            )

            st.stop()


    if not jobs:

        st.warning(
            "No jobs were returned for this search."
        )

        st.info(
            "Try: JavaScript, React, Python "
            "or Web Developer."
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


        if not is_tech_job(
            title,
            description
        ):

            continue


        score, matched_skills, matched_roles = calculate_match(

            user_skills,
            user_roles,
            title,
            description
        )


        missing = find_missing_skills(
            user_skills,
            description
        )


        location_parts = []


        if city:

            location_parts.append(
                city
            )


        if state:

            location_parts.append(
                state
            )


        if country:

            location_parts.append(
                country
            )


        full_location = ", ".join(
            location_parts
        )


        job_text = (
            title
            + " "
            + description
        ).lower()


        # -------------------------------------------------
        # EXPERIENCE FILTER
        # -------------------------------------------------

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
                word in job_text
                for word in keywords
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
                word in job_text
                for word in keywords
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
                word in job_text
                for word in keywords
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
                word in job_text
                for word in keywords
            ):

                continue


        analyzed_jobs.append({

            "title": title,

            "company": company,

            "location": full_location,

            "description": description,

            "employment": employment,

            "apply_link": apply_link,

            "score": score,

            "matched_skills":
                matched_skills,

            "matched_roles":
                matched_roles,

            "missing":
                missing
        })


    # =====================================================
    # SORT
    # =====================================================

    analyzed_jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    if not analyzed_jobs:

        st.warning(
            "Jobs were found but none passed "
            "your selected filters."
        )

        st.info(
            "Try Experience = Any."
        )

        st.stop()


    # =====================================================
    # STATS
    # =====================================================

    total_jobs = len(
        analyzed_jobs
    )

    excellent_jobs = len([
        job
        for job in analyzed_jobs
        if job["score"] >= 75
    ])

    average_score = int(
        sum(
            job["score"]
            for job in analyzed_jobs
        )
        / total_jobs
    )


    st.markdown(
        "## 📊 Search Overview"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">
                    {total_jobs}
                </div>
                <div class="stat-label">
                    Relevant Jobs
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">
                    {excellent_jobs}
                </div>
                <div class="stat-label">
                    Excellent Matches
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="stat-box">
                <div class="stat-value">
                    {average_score}%
                </div>
                <div class="stat-label">
                    Average Match
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # RESULTS
    # =====================================================

    st.markdown(
        "## 🎯 Best Job Matches"
    )


    for index, job in enumerate(
        analyzed_jobs[
            :number_of_jobs
        ],
        start=1
    ):


        score = job["score"]


        if score >= 75:

            match_icon = "🟢"
            match_text = "Excellent Match"

        elif score >= 50:

            match_icon = "🟡"
            match_text = "Good Match"

        elif score >= 25:

            match_icon = "🟠"
            match_text = "Partial Match"

        else:

            match_icon = "🔴"
            match_text = "Low Match"


        st.markdown(
            '<div class="job-box">',
            unsafe_allow_html=True
        )


        left, right = st.columns(
            [5, 1]
        )


        with left:

            st.markdown(
                f"""
                <div class="job-title">
                    {index}. {job["title"]}
                </div>

                <div class="job-company">
                    🏢 {job["company"]}
                </div>

                <div style="
                    color:#cbd5e1;
                    font-size:13px;
                    margin-top:10px;
                ">
                    📍 {job["location"] or "Pakistan"}
                    &nbsp;&nbsp; • &nbsp;&nbsp;
                    💼 {job["employment"]}
                </div>
                """,
                unsafe_allow_html=True
            )


        with right:

            st.markdown(
                f"""
                <div class="match-score">
                    {score}%
                </div>

                <div class="match-text">
                    {match_icon} {match_text}
                </div>
                """,
                unsafe_allow_html=True
            )


        # Matching skills

        if job["matched_skills"]:

            st.markdown(
                '<div class="skill-title">'
                'MATCHING SKILLS'
                '</div>',
                unsafe_allow_html=True
            )

            skills_html = ""

            for skill in job[
                "matched_skills"
            ]:

                skills_html += (
                    f'<span class="skill">'
                    f'✓ {skill}'
                    f'</span>'
                )

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )


        # Matching role

        if job["matched_roles"]:

            st.markdown(
                '<div class="skill-title">'
                'ROLE MATCH'
                '</div>',
                unsafe_allow_html=True
            )

            roles_html = ""

            for role in job[
                "matched_roles"
            ]:

                roles_html += (
                    f'<span class="skill">'
                    f'✓ {role}'
                    f'</span>'
                )

            st.markdown(
                roles_html,
                unsafe_allow_html=True
            )


        # Missing skills

        if job["missing"]:

            st.markdown(
                '<div class="skill-title">'
                'SKILLS TO LEARN'
                '</div>',
                unsafe_allow_html=True
            )

            missing_html = ""

            for skill in job[
                "missing"
            ]:

                missing_html += (
                    f'<span class="missing">'
                    f'+ {skill}'
                    f'</span>'
                )

            st.markdown(
                missing_html,
                unsafe_allow_html=True
            )


        # Description

        if job["description"]:

            with st.expander(
                "📄 View Job Description"
            ):

                st.write(
                    job["description"]
                )


        # Apply

        if job["apply_link"]:

            st.link_button(
                "🚀 Apply Now",
                job["apply_link"],
                use_container_width=False
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        💼 JobPilot AI
        &nbsp; • &nbsp;
        Pakistan Technology Job Search
        &nbsp; • &nbsp;
        Powered by JSearch
    </div>
    """,
    unsafe_allow_html=True
)

