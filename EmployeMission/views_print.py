from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from datetime import datetime

from .models import CLEmployeMission
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user
# fonction pour récupérer l'utilisateur connecté
def generate_employe_mission_pdf(request, mission_id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    employe_mission = get_object_or_404(CLEmployeMission, id=mission_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="employe_mission_{employe_mission.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    # En-tête
    generer_entete_pdf(doc)
    y -= 280

    # Titre
    data_title = [["Fiche Employé-Mission"]]
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
    y -= 100

    # Styles pour paragraphes
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    # Contenu de la fiche
    data = [
        ["Employé", Paragraph(str(employe_mission.employe), normal_style)],
        ["Mission", Paragraph(str(employe_mission.mission).replace('\n', '<br/>'), normal_style)],
        ["Statut", Paragraph(str(employe_mission.statut), normal_style)],
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

    # Pied de page
    generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()

    return response


# ✅ PDF des affectations de mission
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_employes_missions_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    affectations = CLEmployeMission.objects.select_related('employe', 'mission').order_by('employe__tnm', 'employe__tpm')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employes_missions.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 0

    headers = ["Employé", "Mission", "Statut"]
    header_row = [Paragraph(h, styleN) for h in headers]
    col_widths = [130, 250, 90]
    row_height = 20

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 20
        title_table = Table([["Liste des Affectations Employé - Mission"]], colWidths=[width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, width, height)
        title_table.drawOn(doc, 50, y)
        y -=60
        return y

    y = draw_header_and_title()
    current_y = y
    table_data = [header_row]
    last_table_y = 0

    for affectation in affectations:
        row = [
            Paragraph(str(affectation.employe), styleN),
            Paragraph(str(affectation.mission), styleN),
            Paragraph(str(affectation.statut), styleN),
        ]
        table_data.append(row)

        needed_height = row_height * len(table_data)
        if needed_height > current_y - 60:
            table = Table(table_data[:-1], colWidths=col_widths)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ]))
            table.wrapOn(doc, width, height)
            table.drawOn(doc, (width - sum(col_widths)) / 2, current_y - row_height * (len(table_data) - 1))

            doc.showPage()
            current_y = draw_header_and_title()
            table_data = [header_row, row]

    if len(table_data) > 1:
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        table_height = row_height * len(table_data)
        table.wrapOn(doc, width, height)
        table_y = current_y - table_height
        last_table_y = table_y
        table.drawOn(doc, (width - sum(col_widths)) / 2, table_y)

        # ✅ Afficher le total d'affectations
        total_paragraph = Paragraph(
            f"<b>Nombre total d'affectations : {len(affectations)}</b>",
            styleN
        )
        total_paragraph.wrapOn(doc, width, height)
        total_paragraph.drawOn(doc, 60, last_table_y - 30)

    generer_pdf_avec_pied_de_page(doc, username)
    doc.save()
    return response
