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
        ["Unité organisationnelle", str(parcours.organizational_unit)],
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
    ).order_by('stagiaire__tnm', 'stagiaire__tpm')

    filename = f"parcours_stagiaires_{annee}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"; filename*=UTF-8\'\'{quote(filename)}'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    row_height = 25
# Ligne à modifier
    col_widths = [120, 120, 100, 80, 80, 100]  # Largeur réduite des colonnes
    max_width = width - 60
    total_relative = 120 + 120 + 100 + 80 + 80 + 100
    col_widths = [max_width * w / total_relative for w in [120, 120, 100, 80, 80, 100]]


    # Puis dans la création des tableaux, la variable col_widths est utilisée comme avant


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
        return y - 50

    y_start = draw_header_and_title()
    current_y = y_start
    table_data = [header_row]

    for parcours in parcours_list:
        row = [
            Paragraph(str(parcours.stagiaire), style_center),
            Paragraph(str(parcours.organizational_unit), style_center),
            Paragraph(str(parcours.responsable) if parcours.responsable else "Non défini", style_center),
            Paragraph(parcours.date_debut.strftime('%d/%m/%Y') if parcours.date_debut else "N/D", style_center),
            Paragraph(parcours.date_fin.strftime('%d/%m/%Y') if parcours.date_fin else "N/D", style_center),
            Paragraph(parcours.evaluation or "N/A", style_center),
        ]
        table_data.append(row)

        needed_height = row_height * len(table_data)

        # Si on dépasse la zone d'impression verticale
        if needed_height > current_y - 60:
            # Dessiner la table sans la dernière ligne (qui dépasse)
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
            # Commencer nouvelle table avec header + dernière ligne
            table_data = [header_row, row]

    # Dessiner le reste des données si il en reste
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
        table.drawOn(doc, (width - sum(col_widths)) / 2, table_y)

        # Afficher nombre total en bas à gauche
        total_paragraph = Paragraph(f"<b>Nombre total d'enregistrements : {len(parcours_list)}</b>", style_left)
        total_paragraph.wrapOn(doc, width, height)
        total_paragraph.drawOn(doc, 60, table_y - 30)

    elif len(parcours_list) == 0:
        doc.drawString(60, current_y - 20, "Aucun parcours stagiaire enregistré pour l'année en cours.")

    generer_pdf_avec_pied_de_page(doc, username)
    doc.save()
    return response
