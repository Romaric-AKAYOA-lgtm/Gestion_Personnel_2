from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from datetime import datetime

from .models import CLMission
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user


def generate_mission_pdf(request, mission_id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    mission = get_object_or_404(CLMission, id=mission_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mission_{mission.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    generer_entete_pdf(doc)
    y -= 280

    # Titre
    data_title = [["Fiche Mission"]]
    title_table = Table(data_title, colWidths=[300])
    title_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    x_title = (width - 300) / 2
    title_table.wrapOn(doc, width, height)
    title_table.drawOn(doc, x_title, y)
    y -= 180

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    data = [
        ["Employé signataire", Paragraph(str(mission.employe_signataire), normal_style)],
        ["Objet", Paragraph(mission.objet, normal_style)],
        ["Description", Paragraph(mission.description.replace('\n', '<br/>'), normal_style)],
        ["Date début", str(mission.date_debut)],
        ["Date fin", str(mission.date_fin)],
        ["Lieu", mission.lieu_mission],
        ["Organisme", mission.organisme],
        ["Conclusion", Paragraph(mission.conclusion_mission or "N/A", normal_style)],
    ]

    col_widths = [200, 250]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))

    table_width = sum(col_widths)
    x_table = (width - table_width) / 2
    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_table, y)

    generer_pdf_avec_pied_de_page(doc, username)
    doc.showPage()
    doc.save()

    return response

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import redirect

def generate_missions_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    missions = CLMission.objects.select_related('employe_signataire').order_by('-date_debut')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_missions.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1

    headers = ["Objet", "Employé Signataire", "Début", "Fin", "Lieu", "Organisme"]
    col_widths = [100, 100, 60, 60, 80, 80]
    table_width = sum(col_widths)
    row_height = 20
    min_rows_last_page = 4

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 10
        title_table = Table([["Liste des Missions"]], colWidths=[width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        title_table.wrapOn(doc, width, height)
        title_table.drawOn(doc, 50, y)
        return y - 2

    def render_table(data, y_pos):
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        table.wrapOn(doc, width, height)
        x = (width - table_width) / 2
        table.drawOn(doc, x, y_pos - row_height * len(data))

    # 🟩 Affiche l'en-tête UNE SEULE FOIS sur la première page
    y = draw_header_and_title()
    current_y = y
    available_height = current_y - 100  # Marge basse
    rows_per_page = int(available_height / row_height)

    table_data = [[Paragraph(h, styleN) for h in headers]]
    rows_buffered = []

    for i, m in enumerate(missions):
        row = [
            Paragraph(m.objet or "N/A", styleN),
            Paragraph(str(m.employe_signataire) if m.employe_signataire else "N/A", styleN),
            str(m.date_debut) if m.date_debut else "N/A",
            str(m.date_fin) if m.date_fin else "N/A",
            m.lieu_mission or "N/A",
            m.organisme or "N/A"
        ]
        rows_buffered.append(row)
        remaining = len(missions) - (i + 1)

        if len(rows_buffered) == rows_per_page:
            if remaining > min_rows_last_page:
                render_table([[Paragraph(h, styleN) for h in headers]] + rows_buffered, current_y)
                doc.showPage()
                current_y = height - 50  # 🟥 On ne redessine PAS l'en-tête ici
                rows_buffered = []

    if rows_buffered:
        render_table([[Paragraph(h, styleN) for h in headers]] + rows_buffered, current_y)
        y_table = current_y - row_height * (len(rows_buffered) + 1)
        doc.setFont("Times-Roman", 12)
        doc.drawString(50, y_table - 25, f"Nombre d'enregistrements : {len(missions)}")
        generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()
    return response
