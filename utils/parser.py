import pdfplumber


def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

    except Exception:

        return "Invalid or corrupted PDF file."

    return text


def extract_skills(text):

    skills_list = [

        "python",
        "java",
        "c",
        "sql",
        "mysql",
        "html",
        "css",
        "javascript",
        "flask",
        "react",
        "aws",
        "docker",
        "kubernetes",
        "mongodb",
        "machine learning",
        "data structures",
        "dbms"

    ]

    detected_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill in text:

            detected_skills.append(skill)

    return detected_skills


def get_matching_and_missing_skills(
    detected_skills,
    job_description
):

    jd_skills = [

        "python",
        "java",
        "c",
        "sql",
        "mysql",
        "html",
        "css",
        "javascript",
        "flask",
        "react",
        "aws",
        "docker",
        "kubernetes",
        "mongodb",
        "machine learning",
        "data structures",
        "dbms"

    ]

    matching_skills = []
    missing_skills = []

    job_description = job_description.lower()

    required_skills = []

    for skill in jd_skills:

        if skill in job_description:

            required_skills.append(skill)

    for skill in required_skills:

        if skill in detected_skills:

            matching_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(required_skills) > 0:

        ats_score = int(
            (len(matching_skills) / len(required_skills)) * 100
        )

    else:

        ats_score = 0

    return matching_skills, missing_skills, ats_score


def generate_ai_suggestions(
    missing_skills,
    ats_score
):

    suggestions = []

    if ats_score < 50:

        suggestions.append(
            "Your ATS score is low. Add more relevant technical skills."
        )

    if ats_score < 70:

        suggestions.append(
            "Try improving project descriptions with strong action verbs."
        )

    if "flask" in missing_skills:

        suggestions.append(
            "Add Flask projects to strengthen backend development profile."
        )

    if "react" in missing_skills:

        suggestions.append(
            "Learning React can improve frontend opportunities."
        )

    if "docker" in missing_skills:

        suggestions.append(
            "Docker knowledge is highly valuable for deployment roles."
        )

    if "aws" in missing_skills:

        suggestions.append(
            "Add AWS cloud skills and deployment projects."
        )

    if len(missing_skills) > 5:

        suggestions.append(
            "Your resume is missing several important skills from the job description."
        )

    if ats_score >= 80:

        suggestions.append(
            "Excellent resume match. Your profile aligns well with the job description."
        )

    return suggestions