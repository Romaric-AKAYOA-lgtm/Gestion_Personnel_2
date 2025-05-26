from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from .models import CLParcoursStagiaire
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user


def generate_parcours_pdf(request, parcours_id):
    # Vérifier utilisateur connecté
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    parcours = get_object_or_404(CLParcoursStagiaire, id=parcours_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="parcours_{parcours.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    # Entête PDF
    generer_entete_pdf(doc)
    y -= 250

    # Titre
    from reportlab.platypus import Table
    data_title = [["Fiche Parcours Stagiaire"]]
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
    y -= 160

    # Données du parcours
    data = [
        ["Stagiaire", str(parcours.stagiaire)],
        ["Service", str(parcours.organizational_unit)],
        ["Responsable", str(parcours.responsable) if parcours.responsable else "Non défini"],
        ["Date début", parcours.date_debut.strftime('%d/%m/%Y') if parcours.date_debut else "Non défini"],
        ["Date fin", parcours.date_fin.strftime('%d/%m/%Y') if parcours.date_fin else "Non défini"],
        ["Évaluation", parcours.evaluation or "Aucune"],
        ["Commentaire", parcours.commentaire or "Aucun"],
        ["Compétences", parcours.competences or "Aucune"],
    ]

    col_widths = [200, 300]
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
    y -= len(data) * 20 + 20

    # Pied de page
    generer_pdf_avec_pied_de_page(doc, username)

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
from .models import CLParcoursStagiaire
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user
from datetime import datetime
from urllib.parse import quote

def generate_parcours_annee_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    annee = datetime.now().year
    parcours_list = CLParcoursStagiaire.objects.filter(
        date_debut__year=annee
    ).order_by('-date_debut', 'stagiaire__tnm', 'stagiaire__tpm')

    filename = f"parcours_stagiaires_{annee}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"; filename*=UTF-8\'\'{quote(filename)}'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    row_height = 25
    # Colonnes avec largeur relative
    total_relative = 120 + 120 + 100 + 80 + 80 + 100
    max_width = width - 60  # marges gauche/droite
    col_widths = [max_width * w / total_relative for w in [120, 120, 100, 80, 80, 100]]

    styles = getSampleStyleSheet()
    style_center = styles["Normal"].clone('style_center')
    style_center.fontName = 'Times-Roman'
    style_center.fontSize = 10
    style_center.alignment = 1  # center

    style_left = styles["Normal"].clone('style_left')
    style_left.fontName = 'Times-Roman'
    style_left.fontSize = 10
    style_left.alignment = 0  # left

    headers = ["Stagiaire", "Unité org.", "Responsable", "Date début", "Date fin", "Évaluation"]
    header_row = [Paragraph(h, style_center) for h in headers]

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 5
        title = f"Liste des Parcours Stagiaires de l'année {annee}"
        title_table = Table([[title]], colWidths=[width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, width, height)
        title_table.drawOn(doc, 50, y)
        return y - 50  # espace sous le titre

    y_start = draw_header_and_title()
    current_y = y_start

    # Calcul du nombre de lignes par page
    margin_bottom = 60
    available_height = current_y - margin_bottom
    rows_per_page = int(available_height / row_height)
    min_rows_last_page = 5

    rows_buffered = []
    total_rows = len(parcours_list)

    for i, parcours in enumerate(parcours_list):
        row = [
            Paragraph(str(parcours.stagiaire), style_center),
            Paragraph(str(parcours.organizational_unit), style_center),
            Paragraph(str(parcours.responsable) if parcours.responsable else "Non défini", style_center),
            Paragraph(parcours.date_debut.strftime('%d/%m/%Y') if parcours.date_debut else "N/D", style_center),
            Paragraph(parcours.date_fin.strftime('%d/%m/%Y') if parcours.date_fin else "N/D", style_center),
            Paragraph(parcours.evaluation or "N/A", style_center),
        ]
        rows_buffered.append(row)
        remaining = total_rows - (i + 1)

        # Dès que le buffer atteint la limite de lignes par page,
        # et qu'on a assez de lignes restantes pour ne pas couper trop court la dernière page,
        # on imprime la page et on recommence
        if len(rows_buffered) == rows_per_page:
            if remaining > min_rows_last_page:
                table_data = [header_row] + rows_buffered
                table = Table(table_data, colWidths=col_widths, repeatRows=1)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ]))
                table.wrapOn(doc, width, height)
                x_start = (width - sum(col_widths)) / 2
                table.drawOn(doc, x_start, current_y - row_height * len(table_data))
                doc.showPage()
                current_y = draw_header_and_title()
                rows_buffered = []

    # Dernière page, dessiner les lignes restantes
    if rows_buffered:
        table_data = [header_row] + rows_buffered
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
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
        x_start = (width - sum(col_widths)) / 2
        table.drawOn(doc, x_start, current_y - table_height)

        # Afficher nombre total en bas à gauche
        total_paragraph = Paragraph(f"<b>Nombre total d'enregistrements : {total_rows}</b>", style_left)
        total_paragraph.wrapOn(doc, width, height)
        total_paragraph.drawOn(doc, 60, current_y - table_height - 30)
    elif total_rows == 0:
        doc.drawString(60, current_y - 20, "Aucun parcours stagiaire enregistré pour l'année en cours.")

    generer_pdf_avec_pied_de_page(doc, username)
    doc.save()
    return response
