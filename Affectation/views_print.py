from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from Affectation.models import CLAffectation
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user
from datetime import datetime

def generate_affectation_pdf(request, affectation_id):
    # Vérifie si l'utilisateur est connecté
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    # Récupération de l'affectation
    affectation = get_object_or_404(CLAffectation, id=affectation_id)

    # Création de la réponse HTTP pour le fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="affectation_{affectation.id}.pdf"'

    # Initialisation du document PDF
    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    # Entête
    generer_entete_pdf(doc)
    y -= 280

    # Titre
    data_title = [["Fiche d'Affectation"]]
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
    y -= 140

    # Données de l'affectation
    data = [
        ["Employé", str(affectation.employe)],
        ["Organisme affecté", affectation.organisme_affecte],
        ["Lieu d'affectation", affectation.lieu_affectation],
        ["Statut", affectation.statut],
        ["Motif de l'affectation", affectation.motif_affectation],
        ["Date de début", affectation.date_debut.strftime('%d/%m/%Y') if affectation.date_debut else "Non définie"],
        ["Date de fin", affectation.date_fin.strftime('%d/%m/%Y') if affectation.date_fin else "Non définie"],
    ]

    col_widths = [200, 250]
    table_width = sum(col_widths)
    x_table = (width - table_width) / 2

    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))

    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_table, y)

    # Pied de page
    generer_pdf_avec_pied_de_page(doc, username)

    # Finaliser
    doc.showPage()
    doc.save()

    return response
from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from datetime import datetime
from urllib.parse import quote

from Affectation.models import CLAffectation
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user


def generate_affectations_annee_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    annee = datetime.now().year
    affectations = CLAffectation.objects.filter(
        date_debut__year=annee
    ).order_by( '-date_debut', 'employe__tnm', 'employe__tpm')

    filename = f"affectations_{annee}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"; filename*=UTF-8\'\'{quote(filename)}'

    doc = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    row_height = 33

    headers = [
        "Employé", "Organisme Affecté", "Lieu d'Affectation",
        "Statut", "Motif d'Affectation", "Date début", "Date fin"
    ]
    col_widths = [115, 75, 65, 45, 80, 51.5, 51.5]
    table_width = sum(col_widths)

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 10
        title = f"Liste des Affectations de l'Année {annee}"
        title_table = Table([[title]], colWidths=[page_width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, page_width, page_height)
        title_x = (page_width - (page_width - 100)) / 2
        title_table.drawOn(doc, title_x, y)
        return y - 10

    def render_table(doc, data, y_pos):
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        table.wrapOn(doc, page_width, page_height)
        x = (page_width - table_width) / 2
        table.drawOn(doc, x, y_pos - row_height * len(data))

    y = draw_header_and_title()
    current_y = y
    available_height = current_y - 100
    rows_per_page = int(available_height / row_height)
    total_rows = len(affectations)
    min_rows_last_page = 5

    table_data = [[Paragraph(h, styleN) for h in headers]]
    rows_buffered = []

    for i, aff in enumerate(affectations):
        row = [
            Paragraph(f"{aff.employe.tnm or 'N/A'} {aff.employe.tpm or ''}", styleN),
            Paragraph(str(aff.organisme_affecte) if aff.organisme_affecte else "N/A", styleN),
            Paragraph(str(aff.lieu_affectation) if aff.lieu_affectation else "N/A", styleN),
            Paragraph(str(aff.statut) if aff.statut else "N/A", styleN),
            Paragraph(str(aff.motif_affectation) if aff.motif_affectation else "N/A", styleN),
            Paragraph(aff.date_debut.strftime('%d/%m/%Y'), styleN),
            Paragraph(aff.date_fin.strftime('%d/%m/%Y') if aff.date_fin else "Non définie", styleN)
        ]
        rows_buffered.append(row)

        remaining = total_rows - (i + 1)
        if len(rows_buffered) == rows_per_page:
            if remaining > min_rows_last_page:
                render_table(doc, [[Paragraph(h, styleN) for h in headers]] + rows_buffered, current_y)
                doc.showPage()
                current_y = page_height - 50
                rows_buffered = []

    # Dernière page
    if rows_buffered:
        table_data = [[Paragraph(h, styleN) for h in headers]] + rows_buffered
        render_table(doc, table_data, current_y)
        y_table = current_y - row_height * len(table_data)
        doc.setFont("Times-Roman", 12)
        doc.drawString(50, y_table - 25, f"Nombre d'enregistrements : {total_rows}")
        generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()
    return response
