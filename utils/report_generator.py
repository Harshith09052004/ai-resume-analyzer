from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    ats_score,
    matching_skills,
    missing_skills
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "AI Resume Analyzer Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    score = Paragraph(
        f"<b>ATS Score:</b> {ats_score}%",
        styles['BodyText']
    )

    elements.append(score)

    elements.append(Spacer(1, 12))

    matching = Paragraph(
        f"<b>Matching Skills:</b> {', '.join(matching_skills)}",
        styles['BodyText']
    )

    elements.append(matching)

    elements.append(Spacer(1, 12))

    missing = Paragraph(
        f"<b>Missing Skills:</b> {', '.join(missing_skills)}",
        styles['BodyText']
    )

    elements.append(missing)

    doc.build(elements)