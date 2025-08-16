from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from Conge.models import CLConge
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user
from datetime import datetime  # ➤ pour récupérer l'année système


def generate_conge_pdf(request, conge_id):
    # Récupérer l'utilisateur connecté
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    # Récupérer les données du congé
    conge = get_object_or_404(CLConge, id=conge_id)

    # Préparer la réponse HTTP pour retourner un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="conge_{conge.id}.pdf"'

    # Créer le document PDF
    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 80

    # Entête
    generer_entete_pdf(doc)
    y -= 280

    # Titre
    data_title = [["Fiche de Congé"]]
    title_table = Table(data_title, colWidths=[300])  # largeur fixe pour contrôle
    title_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    # Centrage du tableau
    title_table_width = 300
    x_title = (width - title_table_width) / 2
    title_table.wrapOn(doc, width, height)
    title_table.drawOn(doc, x_title, y)
    y -= 120

    # Données du congé
    data = [
        ["Employé", f"{conge.employe.tnm} {conge.employe.tpm}"],
        ["Type de congé", conge.typeconge.designation],
        ["Date début prévisionnelle", conge.date_debut_previsionnel.strftime('%d/%m/%Y')],
        ["Date retour prévisionnelle", conge.date_retour_previsionnel.strftime('%d/%m/%Y')],
        ["Date retour définitif", conge.date_retour_definitif.strftime('%d/%m/%Y') if conge.date_retour_definitif else "Non définie"],
    ]

    col_widths = [200, 250]  # Total = 450
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
    y -= 120

    # Pied de page
    generer_pdf_avec_pied_de_page(doc, username)

    # Finaliser
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
from datetime import datetime
from urllib.parse import quote

from Conge.models import CLConge
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user

def generate_conges_annee_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    annee = datetime.now().year
    conges = CLConge.objects.filter(date_debut_previsionnel__year=annee).order_by('employe__tnm', 'employe__tpm')

    filename = f"conges_{annee}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"; filename*=UTF-8\'\'{quote(filename)}'

    doc = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1  # centré

    styleGauche = styles["Normal"].clone('styleGauche')
    styleGauche.fontName = 'Times-Roman'
    styleGauche.fontSize = 10
    styleGauche.alignment = 0  # gauche

    headers = [
        "Employé",
        "Type de congé",
        "Date début\nprévisionnelle",
        "Date retour\nprévisionnelle",
        "Date retour\ndéfinitif"
    ]
    col_widths = [140, 100, 80, 80, 80]
    table_width = sum(col_widths)
    row_height = 20

    def draw_header_and_title():
        y = generer_entete_pdf(doc)  # logo + infos
        y -= 5
        title_table = Table([[f"Liste des Congés de l'Année {annee}"]], colWidths=[page_width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, page_width, page_height)
        x = (page_width - (page_width - 100)) / 2
        title_table.drawOn(doc, x, y)
        return y - 5

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
    available_height = current_y - 100  # marge inférieure
    rows_per_page = int(available_height / row_height)
    total_rows = len(conges)
    min_rows_last_page = 5  # garder minimum 5 lignes sur dernière page

    header_row = [Paragraph(h.replace('\n', '<br/>'), styleN) for h in headers]
    rows_buffered = []

    for i, conge in enumerate(conges):
        row = [
            Paragraph(f"{conge.employe.tnm} {conge.employe.tpm}", styleN),
            Paragraph(conge.typeconge.designation or "N/A", styleN),
            Paragraph(conge.date_debut_previsionnel.strftime('%d/%m/%Y'), styleN),
            Paragraph(conge.date_retour_previsionnel.strftime('%d/%m/%Y'), styleN),
            Paragraph(conge.date_retour_definitif.strftime('%d/%m/%Y') if conge.date_retour_definitif else "Non définie", styleN)
        ]
        rows_buffered.append(row)

        remaining = total_rows - (i + 1)
        if len(rows_buffered) == rows_per_page:
            if remaining > min_rows_last_page:
                render_table(doc, [header_row] + rows_buffered, current_y)
                doc.showPage()
                current_y = page_height - 50
                rows_buffered = []

    # Dernière page
    if rows_buffered:
        data = [header_row] + rows_buffered
        render_table(doc, data, current_y)
        y_table = current_y - row_height * len(data)
        doc.setFont("Times-Roman", 12)
        doc.drawString(50, y_table - 25, f"Nombre total d'enregistrements : {total_rows}")
        generer_pdf_avec_pied_de_page(doc, username)

    elif total_rows == 0:
        doc.drawString(60, current_y - 20, "Aucun congé enregistré pour l'année en cours.")
        generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()
    return response
