from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

from Employe.models import CLEmploye
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from connection.views import get_connected_user


def generate_employe_pdf(request, employe_id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    employe = get_object_or_404(CLEmploye, id=employe_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="employe_{employe.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 100

    generer_entete_pdf(doc)
    y -= 190

    # Titre
    data_title = [["Fiche Employé(e)"]]
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
    y -= 300

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    data = [
        ["Nom", employe.tnm],
        ["Prénom", employe.tpm or "N/A"],
        ["Matricule", employe.matricule or "N/A"],
        ["Sexe", employe.tsx],
        ["Date de naissance", str(employe.dns)],
        ["Adresse", employe.tads or "N/A"],
        ["Téléphone", employe.tphne or "N/A"],
        ["Email", employe.teml or "N/A"],
        ["Grade", employe.grade or "N/A"],
        ["Échelon", str(employe.echelon) if employe.echelon else "N/A"],
        ["Spécialité", str(employe.specialite) if employe.specialite else "N/A"],
        ["Observation", Paragraph((employe.observation or "Aucune").replace('\n', '<br/>'), normal_style)],
        ["Date début service", str(employe.dsb) if employe.dsb else "N/A"],
        ["Date fin service", str(employe.ddf) if employe.ddf else "N/A"],
        ["Date retraite", str(employe.date_retraite) if employe.date_retraite else "N/A"],
        ["Statut", employe.tstt_user or "N/A"],
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

    x_table = (width - sum(col_widths)) / 2
    table.wrapOn(doc, width, height)
    table.drawOn(doc, x_table, y)

    generer_pdf_avec_pied_de_page(doc, username)
    doc.showPage()
    doc.save()

    return response


def generate_employes_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    employes = CLEmploye.objects.all().order_by('tnm')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_employes.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    generer_entete_pdf(doc)
    y = height - 300

    data_title = [["Liste des Employé(e)s"]]
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
    y -= 80

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10

    headers = ["Nom", "Prénom", "Matricule", "Sexe", "Spécialité", "Grade", "Échelon", "Statut"]
    data = [[Paragraph(h, styleN) for h in headers]]

    for emp in employes:
        data.append([
            emp.tnm,
            emp.tpm or "N/A",
            emp.matricule or "N/A",
            emp.tsx,
            str(emp.specialite) if emp.specialite else "N/A",
            emp.grade or "N/A",
            str(emp.echelon) if emp.echelon else "N/A",
            emp.tstt_user or "N/A",
        ])

    col_widths = [70, 70, 70, 50, 90, 70, 50, 60]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))

    table.wrapOn(doc, width, height)
    table.drawOn(doc, (width - sum(col_widths)) / 2, y)

    y -= len(data) * 20 + 20
    generer_pdf_avec_pied_de_page(doc, username)

    doc.save()
    return response
