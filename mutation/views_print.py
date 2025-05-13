from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from datetime import datetime

from .models import CLMutation
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user

# ✅ PDF détaillé pour une mutation
def generate_mutation_pdf(request, mutation_id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    mutation = get_object_or_404(CLMutation, id=mutation_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mutation_{mutation.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    generer_entete_pdf(doc)
    y -= 280

    # Titre
    data_title = [["Fiche de Mutation"]]
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

    # Données
    data = [
        ["Employé", str(mutation.employe)],
        ["Unité organisationnelle", str(mutation.organizational_unit)],
        ["Fonction", str(mutation.function)],
        ["Responsable", str(mutation.responsable) if mutation.responsable else "Non défini"],
        ["Date de début", mutation.date_debut.strftime('%d/%m/%Y') if mutation.date_debut else "Non définie"],
        ["Date de fin", mutation.date_fin.strftime('%d/%m/%Y') if mutation.date_fin else "Non définie"],
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

    generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()
    return response

# ✅ PDF des mutations de l'année
def generate_mutations_annee_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    annee = datetime.now().year
    mutations = CLMutation.objects.filter(
        date_debut__year=annee
    ).order_by('employe__tnm', 'employe__tpm')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mutations_{annee}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    generer_entete_pdf(doc)
    y = height - 300

    data_title = [["Liste des Mutations de l'Année"]]
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

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10
    styleN.alignment = 1

    headers = [
        "Employé",
        "Unité\nOrganisationnelle",
        "Fonction",
        "Responsable",
        "Date\ndébut",
        "Date\nfin"
    ]

    data = [[Paragraph(h.replace('\n', '<br/>'), styleN) for h in headers]]

    for m in mutations:
        data.append([
            Paragraph(str(m.employe), styleN),
            Paragraph(str(m.organizational_unit), styleN),
            Paragraph(str(m.function), styleN),
            Paragraph(str(m.responsable) if m.responsable else "Non défini", styleN),
            Paragraph(m.date_debut.strftime('%d/%m/%Y') if m.date_debut else "Non définie", styleN),
            Paragraph(m.date_fin.strftime('%d/%m/%Y') if m.date_fin else "Non définie", styleN),
        ])

    col_widths = [90, 100, 80, 90, 60, 60]
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

    table_width = sum(col_widths)
    x_position = (width - table_width) / 2

    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_position, y)

    y -= len(data) * 20 + 20
    generer_pdf_avec_pied_de_page(doc, username)

    doc.save()
    return response
