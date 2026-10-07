
import streamlit as st
import requests
import re
import html


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Pakistan AI Job Search Assistant",
    page_icon="💼",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💼 Pakistan AI Job Search Assistant")

st.write(
    "Find relevant technology jobs in Pakistan based on your skills."
)


# =========================================================
# PAKISTAN CITIES
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


# =========================================================
# TECHNOLOGY KEYWORDS
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

    "html": [
        "html",
        "html5"
    ],

    "css": [
        "css",
        "css3"
    ],

    "javascript": [
        "javascript",
        "js",
        "ecmascript"
    ],

    "typescript": [
        "typescript",
        "ts"
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


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(value):

    if value is None:
        return ""

    text = str(value)

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Convert HTML entities
    text = html.unescape(text)

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# GET USER SKILLS
# =========================================================

def get_user_skills(skill_text):

    skills = []

    for skill in skill_text.split(","):

        skill = skill.strip().lower()

        if skill and skill not in skills:
            skills.append(skill)

    return skills


# =========================================================
# CHECK TECH JOB
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
# CALCULATE MATCH %
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
# FIND MISSING SKILLS
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
# GET JOBS FROM JSEARCH
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
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }


    # -----------------------------------------------------
    # BUILD SEARCH QUERY
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # JSEARCH PARAMETERS
    # -----------------------------------------------------

    params = {

        "query": query,

        "num_pages": "1",

        "country": "pk",

        "language": "en",

        # Use all because month can return 0
        "date_posted": "all"
    }


    # -----------------------------------------------------
    # EMPLOYMENT TYPE
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
    # API REQUEST
    # -----------------------------------------------------

    response = requests.get(

        url,

        headers=headers,

        params=params,

        timeout=30
    )


    # -----------------------------------------------------
    # ERROR CHECK
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
    # GET DATA
    # -----------------------------------------------------

    data = result.get(
        "data",
        []
    )


    # -----------------------------------------------------
    # DATA LIST
    # -----------------------------------------------------

    if isinstance(
        data,
        list
    ):

        return data


    # -----------------------------------------------------
    # DATA DICTIONARY
    # -----------------------------------------------------

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
# READ RAPIDAPI KEY
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
# SKILLS INPUT
# =========================================================

skills_input = st.text_input(

    "💻 Your Skills",

    placeholder=(
        "HTML, CSS, JavaScript, React"
    )
)


# =========================================================
# LOCATION
# =========================================================

location_name = st.selectbox(

    "📍 Job Location",

    list(
        PAKISTAN_CITIES.keys()
    )
)


# =========================================================
# JOB TYPE
# =========================================================

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


# =========================================================
# EXPERIENCE
# =========================================================

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


# =========================================================
# NUMBER OF JOBS
# =========================================================

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

    # -----------------------------------------------------
    # CHECK API KEY
    # -----------------------------------------------------

    if not RAPIDAPI_KEY:

        st.error(
            "RapidAPI key is missing. "
            "Add RAPIDAPI_KEY in "
            "Streamlit Secrets."
        )

        st.stop()


    # -----------------------------------------------------
    # CHECK SKILLS
    # -----------------------------------------------------

    if not skills_input.strip():

        st.warning(
            "Please enter your skills first."
        )

        st.stop()


    # -----------------------------------------------------
    # USER SKILLS
    # -----------------------------------------------------

    user_skills = get_user_skills(
        skills_input
    )


    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    selected_location = (
        PAKISTAN_CITIES[
            location_name
        ]
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # NO JOBS
    # -----------------------------------------------------

    if not jobs:

        st.warning(
            "JSearch returned no jobs "
            "for this search."
        )

        st.info(
            "Try broader skills such as "
            "JavaScript, Python, React "
            "or Software Developer."
        )

        st.stop()


    # =====================================================
    # ANALYZE JOBS
    # =====================================================

    analyzed_jobs = []


    for job in jobs:

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------

        if not isinstance(
            job,
            dict
        ):

            continue


        # -------------------------------------------------
        # JOB INFORMATION
        # -------------------------------------------------

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


        # -------------------------------------------------
        # TITLE CHECK
        # -------------------------------------------------

        if not title:

            continue


        # -------------------------------------------------
        # TECH JOB FILTER
        # -------------------------------------------------

        if not is_tech_job(
            title,
            description
        ):

            continue


        # -------------------------------------------------
        # MATCH SCORE
        # -------------------------------------------------

        score, matched = calculate_match(

            user_skills,

            title,

            description
        )


        # -------------------------------------------------
        # MISSING SKILLS
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


        # -------------------------------------------------
        # EXPERIENCE FILTER
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
        # SAVE JOB
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
    # SORT BY MATCH
    # =====================================================

    analyzed_jobs.sort(

        key=lambda x: x["score"],

        reverse=True
    )


    # =====================================================
    # EMPTY AFTER FILTER
    # =====================================================

    if not analyzed_jobs:

        st.warning(
            "Jobs were returned by JSearch, "
            "but none passed our technology "
            "or experience filter."
        )

        st.info(
            "Try Experience = Any and "
            "use JavaScript, React, Python "
            "or Software Developer."
        )

        st.stop()


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(

        f"Found "
        f"{len(analyzed_jobs)} "
        f"relevant jobs."
    )


    # =====================================================
    # JOB RESULTS
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

            label = (
                "🟢 Excellent Match"
            )

        elif score >= 50:

            label = (
                "🟡 Good Match"
            )

        elif score >= 25:

            label = (
                "🟠 Partial Match"
            )

        else:

            label = (
                "🔴 Low Match"
            )


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

                f"### {label} — "
                f"{score}%"

            )


            # -------------------------------------------------
            # MATCHING SKILLS
            # -------------------------------------------------

            if job["matched"]:

                st.write(

                    "✅ **Matching skills:** "
                    + ", ".join(
                        job["matched"]
                    )

                )


            # -------------------------------------------------
            # MISSING SKILLS
            # -------------------------------------------------

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


            # -------------------------------------------------
            # DESCRIPTION
            # -------------------------------------------------

            if job["description"]:

                with st.expander(
                    "📄 Job Description"
                ):

                    st.write(
                        job["description"]
                    )


            # -------------------------------------------------
            # APPLY
            # -------------------------------------------------

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
    "| JSearch + Intelligent Skills Matching"

)
