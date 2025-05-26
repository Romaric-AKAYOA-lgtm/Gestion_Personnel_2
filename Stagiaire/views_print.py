from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from pandas import read_table
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

from connection.views import get_connected_user
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from .models import CLStagiaire


def generate_stagiaire_pdf(request, stagiaire_id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    stagiaire = get_object_or_404(CLStagiaire, id=stagiaire_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="stagiaire_{stagiaire.id}.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 100

    generer_entete_pdf(doc)
    y -= 190

    title_table = Table([["Fiche Stagiaire"]], colWidths=[300])
    title_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    title_table.wrapOn(doc, width, height)
    title_table.drawOn(doc, (width - 300) / 2, y)
    y -= 200

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    data = [
        ["Nom", stagiaire.tnm or "N/A"],
        ["Prénom", stagiaire.tpm or "N/A"],
        ["Sexe", stagiaire.tsx or "N/A"],
        ["Date de naissance", str(stagiaire.dns) if stagiaire.dns else "N/A"],
        ["Téléphone", stagiaire.tphne or "N/A"],
        ["Email", stagiaire.teml or "N/A"],
        ["Etablissement", stagiaire.etablissement or "N/A"],
        ["Filière", stagiaire.filiere or "N/A"],
        ["Thème de stage", Paragraph((stagiaire.theme or "N/A").replace('\n', '<br/>'), normal_style)],
        ["Statut", stagiaire.tstt_user or "N/A"],
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

    table.wrapOn(doc, width, height)
    table.drawOn(doc, (width - sum(col_widths)) / 2, y)

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

from connection.views import get_connected_user
from Gestion_Personnel_2.views_print import generer_entete_pdf, generer_pdf_avec_pied_de_page
from .models import CLStagiaire

def generate_stagiaires_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    stagiaires = CLStagiaire.objects.all().order_by('-dsb')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_stagiaires.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10

    headers = ["Nom", "Prénom", "Sexe", "Téléphone", "Email", "Établissement", "Filière", "Statut"]
    col_widths = [65, 65, 40, 70, 80, 90, 80, 60]
    table_width = sum(col_widths)
    row_height = 20

    def render_title(doc, y):
        title_table = Table([["Liste des Stagiaires"]], colWidths=[page_width - 100])
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
        return y - 30

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

    # Première page : entête et titre
    y = generer_entete_pdf(doc)
    y = render_title(doc, y)
    current_y = y
    available_height = current_y - 100  # Marge inférieure
    rows_per_page = int(available_height / row_height)
    total_rows = len(stagiaires)
    min_rows_last_page = 5  # Minimum pour la dernière page

    table_data = [[Paragraph(h, styleN) for h in headers]]
    rows_buffered = []

    for i, st in enumerate(stagiaires):
        row = [
            Paragraph(st.tnm or "N/A", styleN),
            Paragraph(st.tpm or "N/A", styleN),
            Paragraph(st.tsx or "N/A", styleN),
            Paragraph(st.tphne or "N/A", styleN),
            Paragraph(st.teml or "N/A", styleN),
            Paragraph(st.etablissement or "N/A", styleN),
            Paragraph(st.filiere or "N/A", styleN),
            Paragraph(st.tstt_user or "N/A", styleN),
        ]
        rows_buffered.append(row)

        remaining = total_rows - (i + 1)
        if len(rows_buffered) == rows_per_page:
            if remaining > min_rows_last_page:
                render_table(doc, [[Paragraph(h, styleN) for h in headers]] + rows_buffered, current_y)
                doc.showPage()
                current_y = page_height - 50  # En-tête ignorée sur les pages suivantes
                rows_buffered = []

    if rows_buffered:
        y=10
        table_data = [[Paragraph(h, styleN) for h in headers]] + rows_buffered
        render_table(doc, table_data, current_y)
        y_table = current_y - row_height * len(table_data)
        doc.setFont("Times-Roman", 12)
        doc.drawString(50, y_table - 30, f"Nombre d'enregistrements : {total_rows}")
        generer_pdf_avec_pied_de_page(doc, username)

    doc.showPage()
    doc.save()
    return response
