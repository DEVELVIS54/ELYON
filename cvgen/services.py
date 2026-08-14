import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer,
                                 Table, TableStyle)


def build_cv_pdf(profile):
    """Génère un CV professionnel en PDF à partir d'un Profile ELYON."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    accent = colors.HexColor(profile.primary_color or '#E8231A')

    name_style = ParagraphStyle(
        'Name', parent=styles['Title'], fontSize=22, textColor=accent, spaceAfter=2,
    )
    role_style = ParagraphStyle(
        'Role', parent=styles['Normal'], fontSize=13, textColor=colors.HexColor('#444444'),
        spaceAfter=10,
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'], fontSize=13, textColor=accent,
        spaceBefore=14, spaceAfter=6, borderPadding=0,
    )
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=colors.grey)

    elements = []

    elements.append(Paragraph(profile.full_name or profile.user.username, name_style))
    elements.append(Paragraph(profile.profession or '', role_style))

    contact_bits = [b for b in [
        profile.email_public, profile.phone, profile.location,
    ] if b]
    if contact_bits:
        elements.append(Paragraph(" · ".join(contact_bits), small_style))
    elements.append(Spacer(1, 8))

    if profile.bio:
        elements.append(Paragraph("PROFIL", section_style))
        elements.append(Paragraph(profile.bio, body_style))

    experiences = profile.experiences.all()
    if experiences:
        elements.append(Paragraph("EXPÉRIENCES", section_style))
        for exp in experiences:
            end = "Présent" if exp.is_current else (exp.end_date.strftime('%m/%Y') if exp.end_date else '')
            header = f"<b>{exp.title}</b> — {exp.company} ({exp.start_date.strftime('%m/%Y')} - {end})"
            elements.append(Paragraph(header, body_style))
            if exp.description:
                elements.append(Paragraph(exp.description, small_style))
            elements.append(Spacer(1, 4))

    educations = profile.educations.all()
    if educations:
        elements.append(Paragraph("FORMATIONS", section_style))
        for edu in educations:
            end = edu.end_date.strftime('%m/%Y') if edu.end_date else 'en cours'
            header = f"<b>{edu.degree}</b> — {edu.school} ({edu.start_date.strftime('%m/%Y')} - {end})"
            elements.append(Paragraph(header, body_style))
            elements.append(Spacer(1, 4))

    skills = profile.skills.all()
    if skills:
        elements.append(Paragraph("COMPÉTENCES", section_style))
        elements.append(Paragraph(", ".join(s.name for s in skills), body_style))

    social_links = profile.social_links.all()
    if social_links:
        elements.append(Paragraph("LIENS", section_style))
        links_text = " · ".join(f"{l.get_platform_display()}: {l.url}" for l in social_links)
        elements.append(Paragraph(links_text, small_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer
