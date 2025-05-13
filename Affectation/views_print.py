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

from Affectation.models import CLAffectation
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user

def generate_affectations_annee_pdf(request):
    # Vérifie que l'utilisateur est connecté
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    # Obtenir l'année système actuelle
    annee = datetime.now().year

    # Récupérer les affectations de l'année en cours (sur la base de la date_debut)
    affectations = CLAffectation.objects.filter(
        date_debut__year=annee
    ).order_by('employe__tnm', 'employe__tpm')

    # Préparer la réponse HTTP pour fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="affectations_{annee}.pdf"'

    # Création du document PDF
    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Entête
    generer_entete_pdf(doc)
    y = height - 300

    # Titre
    data_title = [["Liste des Affectations de l'Année"]]
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
    y -= 100

    # Styles pour Paragraph
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1  # Centré

    # En-têtes
    headers = [
        "Employé",
        "Organisme\nAffecté",
        "Lieu\nd'Affectation",
        "Statut",
        "Motif\nd'Affectation",
        "Date\ndébut",
        "Date\nfin"
    ]

    data = [[Paragraph(h.replace('\n', '<br/>'), styleN) for h in headers]]

    # Données de chaque affectation
    for aff in affectations:
        data.append([
            Paragraph(f"{aff.employe.tnm} {aff.employe.tpm}", styleN),
            Paragraph(str(aff.organisme_affecte), styleN),
            Paragraph(str(aff.lieu_affectation), styleN),
            Paragraph(str(aff.statut), styleN),
            Paragraph(str(aff.motif_affectation), styleN),
            Paragraph(aff.date_debut.strftime('%d/%m/%Y') if aff.date_debut else "Non définie", styleN),
            Paragraph(aff.date_fin.strftime('%d/%m/%Y') if aff.date_fin else "Non définie", styleN),
        ])

    # Largeur des colonnes
    col_widths = [90, 90, 90, 60, 100, 60, 60]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ]))

    # Centrage horizontal
    table_width = sum(col_widths)
    x_position = (width - table_width) / 2

    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_position, y)

    # Espace en fonction du nombre de lignes
    y -= len(data) * 20 + 20

    # Pied de page
    generer_pdf_avec_pied_de_page(doc, username)

    # Sauvegarde finale
    doc.save()
    return response
