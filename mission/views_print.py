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

def generate_missions_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    missions = CLMission.objects.select_related('employe_signataire').order_by('date_debut')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_missions.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    generer_entete_pdf(doc)
    y = height - 300

    data_title = [["Liste des Missions"]]
    title_table = Table(data_title, colWidths=[width - 100])
    title_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    title_table.wrapOn(doc, width, height)
    title_table.drawOn(doc, 50, y)
    y -= 120

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1

    headers = ["Objet", "Employé Signataire", "Début", "Fin", "Lieu", "Organisme"]
    data = [[Paragraph(h, styleN) for h in headers]]

    for m in missions:
        data.append([
            Paragraph(m.objet, styleN),
            Paragraph(str(m.employe_signataire), styleN),
            str(m.date_debut),
            str(m.date_fin),
            m.lieu_mission,
            m.organisme
        ])

    col_widths = [100, 100, 60, 60, 80, 80]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))

    table_width = sum(col_widths)
    x_position = (width - table_width) / 2
    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_position, y)

    y -= len(data) * 20 + 20
    generer_pdf_avec_pied_de_page(doc, username)

    doc.save()
    return response
