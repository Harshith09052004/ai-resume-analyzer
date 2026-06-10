from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_report(
    filename,
    ats_score,
    matching_skills,
    missing_skills,
    suggestions=None
):

    if suggestions is None:
        suggestions = []

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "AI Resume Analyzer - ATS Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    score_color = "green" if ats_score >= 70 else "red"

    score = Paragraph(
        f"<font color='{score_color}'><b>ATS Score: {ats_score}%</b></font>",
        styles['Heading2']
    )

    elements.append(score)
    elements.append(Spacer(1, 20))

    matching = Paragraph(
        f"<b>Matching Skills:</b><br/>{', '.join(matching_skills)}",
        styles['BodyText']
    )

    elements.append(matching)
    elements.append(Spacer(1, 15))

    missing = Paragraph(
        f"<b>Missing Skills:</b><br/>{', '.join(missing_skills)}",
        styles['BodyText']
    )

    elements.append(missing)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b>AI Recommendations</b>",
            styles['Heading2']
        )
    )

    elements.append(Spacer(1, 10))

    if suggestions:

        for suggestion in suggestions:

            elements.append(
                Paragraph(
                    f"• {suggestion}",
                    styles['BodyText']
                )
            )

            elements.append(Spacer(1, 5))

    else:

        elements.append(
            Paragraph(
                "No recommendations available.",
                styles['BodyText']
            )
        )

    elements.append(Spacer(1, 20))

    verdict = "Excellent Match" if ats_score >= 80 else \
              "Good Match" if ats_score >= 60 else \
              "Needs Improvement"

    elements.append(
        Paragraph(
            f"<b>Final Verdict:</b> {verdict}",
            styles['Heading2']
        )
    )

    doc.build(elements)