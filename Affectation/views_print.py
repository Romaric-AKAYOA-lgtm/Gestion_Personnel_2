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
    ).order_by('employe__tnm', 'employe__tpm')

    filename = f"affectations_{annee}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"; filename*=UTF-8\'\'{quote(filename)}'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Marges précises de 2 cm = 56.7 points
    marge_gauche = marge_droite = 56.7
    largeur_utilisable = width - marge_gauche - marge_droite  # ≈ 481.87 pts

    # Ajustement des colonnes pour tenir dans largeur_utilisable
    col_widths = [115, 75, 65, 45, 80, 51.5, 51.5]  # Total ≈ 483 pts (légèrement arrondi)

    row_height = 25

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1  # Centré

    styleGauche = styles["Normal"].clone('styleGauche')
    styleGauche.fontName = 'Times-Roman'
    styleGauche.fontSize = 10
    styleGauche.alignment = 0

    headers = [
        "Employé",
        "Organisme\nAffecté",
        "Lieu\nd'Affectation",
        "Statut",
        "Motif\nd'Affectation",
        "Date\ndébut",
        "Date\nfin"
    ]
    header_row = [Paragraph(h.replace('\n', '<br/>'), styleN) for h in headers]

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 10
        title_table = Table([[f"Liste des Affectations de l'Année {annee}"]],
                            colWidths=[largeur_utilisable])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, width, height)
        title_table.drawOn(doc, marge_gauche, y)
        y -= 30
        return y

    y = draw_header_and_title()
    current_y = y
    table_data = [header_row]

    for aff in affectations:
        row = [
            Paragraph(f"{aff.employe.tnm} {aff.employe.tpm}", styleN),
            Paragraph(str(aff.organisme_affecte) or "N/A", styleN),
            Paragraph(str(aff.lieu_affectation) or "N/A", styleN),
            Paragraph(str(aff.statut) or "N/A", styleN),
            Paragraph(str(aff.motif_affectation) or "N/A", styleN),
            Paragraph(aff.date_debut.strftime('%d/%m/%Y'), styleN),
            Paragraph(aff.date_fin.strftime('%d/%m/%Y') if aff.date_fin else "Non définie", styleN)
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
            table.drawOn(doc, marge_gauche, current_y - row_height * (len(table_data) - 1))

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
        table.drawOn(doc, marge_gauche, table_y)

        total_paragraph = Paragraph(f"<b>Nombre total d'enregistrements : {len(affectations)}</b>", styleGauche)
        total_paragraph.wrapOn(doc, width, height)
        total_paragraph.drawOn(doc, marge_gauche, table_y - 30)

    elif len(affectations) == 0:
        doc.drawString(marge_gauche, current_y - 20, "Aucune affectation enregistrée pour l'année en cours.")

    generer_pdf_avec_pied_de_page(doc, username)
    doc.save()
    return response
