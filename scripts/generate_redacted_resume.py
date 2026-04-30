from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATH = ROOT / "src" / "cyberfolio" / "content.py"
CONTENT_SPEC = importlib.util.spec_from_file_location("cyberfolio_content", CONTENT_PATH)
if CONTENT_SPEC is None or CONTENT_SPEC.loader is None:
    raise RuntimeError(f"Unable to load content module from {CONTENT_PATH}")

content = importlib.util.module_from_spec(CONTENT_SPEC)
sys.modules["cyberfolio_content"] = content
CONTENT_SPEC.loader.exec_module(content)

CERTIFICATIONS = content.CERTIFICATIONS
EDUCATION = content.EDUCATION
EXPERIENCE = content.EXPERIENCE
REDIRECTED_RESUME_FILENAME = content.REDIRECTED_RESUME_FILENAME
SKILL_GROUPS = content.SKILL_GROUPS
SOCIAL_LINKS = content.SOCIAL_LINKS


def build_resume(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.6 * inch,
        title="Vishnu Gangula Resume (Redacted)",
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14,
            textColor=colors.HexColor("#0b4f6c"),
            spaceAfter=8,
            spaceBefore=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="RoleHeading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.black,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCopy",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=13,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TopMeta",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1f2933"),
        )
    )

    story: list = []
    story.append(Paragraph("Vishnu Gangula", styles["Title"]))

    public_links = " | ".join(
        f'{link["label"]}: <link href="{link["url"]}">{link["display"]}</link>'
        for link in SOCIAL_LINKS
    )
    story.append(Paragraph(public_links, styles["TopMeta"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Education", styles["SectionHeading"]))
    story.append(Paragraph(EDUCATION["school"], styles["RoleHeading"]))
    story.append(Paragraph(EDUCATION["dates"], styles["BodyCopy"]))
    story.append(Paragraph(EDUCATION["degree"], styles["BodyCopy"]))

    story.append(Paragraph("Experience", styles["SectionHeading"]))
    for role in EXPERIENCE:
        story.append(Paragraph(role["role"], styles["RoleHeading"]))
        story.append(
            Paragraph(
                f'{role["company"]} | {role["location"]} | {role["dates"]}',
                styles["BodyCopy"],
            )
        )
        story.append(Paragraph(role["summary"], styles["BodyCopy"]))
        bullet_items = [
            ListItem(Paragraph(bullet, styles["BodyCopy"]), leftIndent=10)
            for bullet in role["bullets"]
        ]
        story.append(
            ListFlowable(
                bullet_items,
                bulletType="bullet",
                start="circle",
                leftIndent=14,
                bulletFontName="Helvetica",
            )
        )
        story.append(Spacer(1, 8))

    story.append(Paragraph("Certifications", styles["SectionHeading"]))
    for cert in CERTIFICATIONS:
        story.append(
            Paragraph(
                f'<b>{cert["name"]}</b> - {cert["status"]}',
                styles["BodyCopy"],
            )
        )
        story.append(Paragraph(cert["details"], styles["BodyCopy"]))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Skills", styles["SectionHeading"]))
    for group in SKILL_GROUPS:
        items = ", ".join(group["items"])
        story.append(Paragraph(f'<b>{group["title"]}:</b> {items}', styles["BodyCopy"]))
        story.append(Spacer(1, 3))

    doc.build(story)


if __name__ == "__main__":
    build_resume(ROOT / "src" / "cyberfolio" / "static" / REDIRECTED_RESUME_FILENAME)
