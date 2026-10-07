
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

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(99, 102, 241, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(14, 165, 233, 0.10),
            transparent 25%
        ),
        #0b1020;
    color: #f8fafc;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f8fafc;
}

/* Main */

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hero */

.hero {
    padding: 35px 38px;
    border: 1px solid #26324a;
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(15, 23, 42, 0.85)
        );
    margin-bottom: 25px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.22);
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(99,102,241,0.14);
    border: 1px solid rgba(129,140,248,0.30);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.hero h1 {
    font-size: 42px;
    line-height: 1.1;
    margin: 0;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero p {
    color: #94a3b8;
    font-size: 16px;
    margin-top: 13px;
    max-width: 700px;
    line-height: 1.7;
}

/* Search box */

.search-panel {
    background: rgba(15,23,42,0.85);
    border: 1px solid #26324a;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 28px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #6366f1;
    background: linear-gradient(
        135deg,
        #6366f1,
        #4f46e5
    );
    color: white;
    font-weight: 700;
    padding: 11px 20px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.25);
}

/* Inputs */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #111827 !important;
    border-color: #334155 !important;
    border-radius: 10px !important;
}

input {
    color: white !important;
}

/* Section */

.section-title {
    font-size: 25px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 16px;
}

/* Job Card */

.job-card {
    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.98),
        rgba(15,23,42,0.95)
    );
    border: 1px solid #273449;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.job-title {
    color: #f8fafc;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 5px;
}

.company {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 15px;
}

.meta {
    color: #cbd5e1;
    font-size: 13px;
    margin-bottom: 8px;
}

/* Match */

.match-box {
    text-align: center;
    padding: 13px 18px;
    border-radius: 14px;
    background: rgba(99,102,241,0.10);
    border: 1px solid rgba(99,102,241,0.25);
}

.match-number {
    font-size: 30px;
    font-weight: 800;
    color: #a5b4fc;
}

.match-label {
    color: #94a3b8;
    font-size: 12px;
}

/* Skill chips */

.skill-chip {
    display: inline-block;
    padding: 5px 10px;
    margin: 3px;
    border-radius: 999px;
    background: #172554;
    color: #bfdbfe;
    border: 1px solid #1e40af;
    font-size: 12px;
}

.missing-chip {
    display: inline-block;
    padding: 5px 10px;
    margin: 3px;
    border-radius: 999px;
    background: #3f1d24;
    color: #fda4af;
    border: 1px solid #7f1d1d;
    font-size: 12px;
}

/* Stats */

.stat-card {
    background: rgba(15,23,42,0.85);
    border: 1px solid #26324a;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}

.stat-number {
    font-size: 27px;
    font-weight: 800;
    color: #a5b4fc;
}

.stat-label {
    color: #94a3b8;
    font-size: 12px;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)


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
    "api": ["api", "rest api", "restful api"],
    "redux": ["redux"],
    "nextjs": ["next.js", "nextjs"],
    "tailwind": ["tailwind", "tailwind css"],
    "bootstrap": ["bootstrap"],
    "docker": ["docker"],
    "aws": ["aws"],
    "azure": ["azure"],
    "flutter": ["flutter"],
    "react native": ["react native"]
}


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


def get_user_skills(skill_text):

    skills = []

    for skill in skill_text.split(","):

        skill = skill.strip().lower()

        if skill and skill not in skills:
            skills.append(skill)

    return skills


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
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    if skills:

        skill_query = " ".join(
            skills[:3]
        )

    else:

        skill_query = "software developer"

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
        "date_posted": "all"
    }

    if job_type == "Full-time":

        params["employment_types"] = "FULLTIME"

    elif job_type == "Part-time":

        params["employment_types"] = "PARTTIME"

    elif job_type == "Internship":

        params["employment_types"] = "INTERN"

    elif job_type == "Contract":

        params["employment_types"] = "CONTRACTOR"

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

    try:

        result = response.json()

    except Exception:

        raise Exception(
            "JSearch returned invalid JSON."
        )

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
        """
        <div style="
            font-size:26px;
            font-weight:800;
            margin-bottom:5px;
        ">
            💼 JobPilot AI
        </div>
        """,
        unsafe_allow_html=True
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
        15
    )

    st.divider()

    st.markdown(
        """
        **How it works**

        1. Enter your skills
        2. Select your preferred location
        3. Search live job listings
        4. Compare skill matches
        5. Identify skills to learn
        6. Apply directly
        """
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-POWERED CAREER ASSISTANT
        </div>

        <h1>
            Find your next opportunity.
        </h1>

        <p>
            Search technology jobs across Pakistan,
            discover how well your skills match,
            identify missing skills, and apply faster.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SEARCH PANEL
# =========================================================

st.markdown(
    '<div class="search-panel">',
    unsafe_allow_html=True
)

st.markdown(
    "### 🔎 What can you do?",
)

skills_input = st.text_input(
    "Your skills",
    placeholder=(
        "e.g. HTML, CSS, JavaScript, React, Figma"
    ),
    label_visibility="collapsed"
)

search_clicked = st.button(
    "🚀  Find My Best Jobs",
    type="primary"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# SEARCH
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
            "Please enter at least one skill."
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


    with st.spinner(
        "🔎 Finding the best jobs for you..."
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


    if not jobs:

        st.warning(
            "No jobs were returned for this search."
        )

        st.info(
            "Try broader skills such as "
            "JavaScript, Python, React or "
            "Software Developer."
        )

        st.stop()


    # =====================================================
    # ANALYZE JOBS
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


        score, matched = calculate_match(
            user_skills,
            title,
            description
        )


        missing = find_missing_skills(
            user_skills,
            description
        )


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


        job_text = (
            title
            + " "
            + description
        ).lower()


        # Experience filter

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


    if not analyzed_jobs:

        st.warning(
            "Jobs were found, but none matched "
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
        '<div class="section-title">📊 Search Overview</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-number">
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
            <div class="stat-card">

                <div class="stat-number">
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
            <div class="stat-card">

                <div class="stat-number">
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
        '<div class="section-title">🎯 Best Job Matches</div>',
        unsafe_allow_html=True
    )


    for index, job in enumerate(
        analyzed_jobs[:number_of_jobs],
        start=1
    ):

        score = job["score"]


        if score >= 75:

            label = "Excellent Match"
            icon = "🟢"

        elif score >= 50:

            label = "Good Match"
            icon = "🟡"

        elif score >= 25:

            label = "Partial Match"
            icon = "🟠"

        else:

            label = "Low Match"
            icon = "🔴"


        st.markdown(
            '<div class="job-card">',
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(
            [5, 1]
        )


        with col1:

            st.markdown(
                f"""
                <div class="job-title">
                    {index}. {job["title"]}
                </div>

                <div class="company">
                    🏢 {job["company"]}
                </div>

                <div class="meta">
                    📍 {job["location"] or "Pakistan"}
                    &nbsp;&nbsp; • &nbsp;&nbsp;
                    💼 {job["employment"]}
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
                <div class="match-box">

                    <div class="match-number">
                        {score}%
                    </div>

                    <div class="match-label">
                        {icon} {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # Matching skills

        if job["matched"]:

            chips = ""

            for skill in job["matched"]:

                chips += (
                    f'<span class="skill-chip">'
                    f'✓ {skill}'
                    f'</span>'
                )


            st.markdown(
                f"""
                <div style="margin-top:18px;">
                    <div style="
                        color:#94a3b8;
                        font-size:12px;
                        margin-bottom:7px;
                    ">
                        MATCHING SKILLS
                    </div>

                    {chips}
                </div>
                """,
                unsafe_allow_html=True
            )


        # Missing skills

        if job["missing"]:

            chips = ""

            for skill in job["missing"]:

                chips += (
                    f'<span class="missing-chip">'
                    f'+ {skill}'
                    f'</span>'
                )


            st.markdown(
                f"""
                <div style="margin-top:14px;">
                    <div style="
                        color:#94a3b8;
                        font-size:12px;
                        margin-bottom:7px;
                    ">
                        SKILLS TO LEARN
                    </div>

                    {chips}
                </div>
                """,
                unsafe_allow_html=True
            )


        # Description

        if job["description"]:

            with st.expander(
                "📄 View job description"
            ):

                st.write(
                    job["description"]
                )


        # Apply

        if job["apply_link"]:

            st.link_button(
                "🚀 Apply Now",
                job["apply_link"]
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

