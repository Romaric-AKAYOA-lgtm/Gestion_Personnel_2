from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

from connection.views import get_connected_user
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from .models import CLEmploye


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

    # Titre du document
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


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import redirect

def generate_employes_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    employes = CLEmploye.objects.all().order_by('tnm')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_employes.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10

    headers = ["Nom", "Prénom", "Matricule", "Sexe", "Spécialité", "Grade", "Échelon", "Statut"]
    col_widths = [70, 70, 70, 50, 95, 70, 50, 60]
    table_width = sum(col_widths)
    row_height = 20

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 5
        title_table = Table([["Liste des Employé(e)s"]], colWidths=[page_width - 100])
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
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        table.wrapOn(doc, page_width, page_height)
        x = (page_width - table_width) / 2
        table.drawOn(doc, x, y_pos - row_height * len(data))

    y = draw_header_and_title()
    current_y = y
    available_height = current_y - 100  # Marge inférieure
    rows_per_page = int(available_height / row_height)
    total_rows = len(employes)
    min_rows_last_page = 5  # Minimum à garder avec pied de page

    table_data = [[Paragraph(h, styleN) for h in headers]]
    rows_buffered = []

    for i, emp in enumerate(employes):
        row = [
            Paragraph(emp.tnm or "N/A", styleN),
            Paragraph(emp.tpm or "N/A", styleN),
            Paragraph(emp.matricule or "N/A", styleN),
            Paragraph(emp.tsx or "N/A", styleN),
            Paragraph(str(emp.specialite) if emp.specialite else "N/A", styleN),
            Paragraph(emp.grade or "N/A", styleN),
            Paragraph(str(emp.echelon) if emp.echelon else "N/A", styleN),
            Paragraph(emp.tstt_user or "N/A", styleN),
        ]
        rows_buffered.append(row)

        remaining = total_rows - (i + 1)
        if len(rows_buffered) == rows_per_page:
            # Si on peut garder suffisamment pour la dernière page
            if remaining > min_rows_last_page:
                render_table(doc, [[Paragraph(h, styleN) for h in headers]] + rows_buffered, current_y)
                doc.showPage()
                current_y = page_height - 50
                rows_buffered = []

    # Dernière page : affiche les lignes restantes et pied de page
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
