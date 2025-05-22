from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
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

    stagiaires = CLStagiaire.objects.all().order_by('tnm')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_stagiaires.pdf"'

    doc = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4

    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 10

    headers = ["Nom", "Prénom", "Sexe", "Téléphone", "Email", "Etablissement", "Filière", "Statut"]
    col_widths = [65, 65, 40, 70, 80, 90, 80, 60]
    table_width = sum(col_widths)
    row_height = 20

    def draw_header_and_title():
        y = generer_entete_pdf(doc)
        y -= 5
        title_table = Table([["Liste des Stagiaires"]], colWidths=[page_width - 100])
        title_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        title_table.wrapOn(doc, page_width, page_height)
        title_table.drawOn(doc, 50, y)
        return y - 50

    y = draw_header_and_title()
    current_y = y
    table_data = [[Paragraph(h, styleN) for h in headers]]

    for stagiaire in stagiaires:
        row = [
            Paragraph(stagiaire.tnm or "N/A", styleN),
            Paragraph(stagiaire.tpm or "N/A", styleN),
            Paragraph(stagiaire.tsx or "N/A", styleN),
            Paragraph(stagiaire.tphne or "N/A", styleN),
            Paragraph(stagiaire.teml or "N/A", styleN),
            Paragraph(stagiaire.etablissement or "N/A", styleN),
            Paragraph(stagiaire.filiere or "N/A", styleN),
            Paragraph(stagiaire.tstt_user or "N/A", styleN),
        ]
        table_data.append(row)

        if current_y - row_height * len(table_data) < 100:
            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ]))
            table.wrapOn(doc, page_width, page_height)
            x = (page_width - table_width) / 2
            table.drawOn(doc, x, current_y - row_height * len(table_data))

            generer_pdf_avec_pied_de_page(doc, username)
            doc.showPage()
            current_y = draw_header_and_title()
            table_data = [[Paragraph(h, styleN) for h in headers]]

    if len(table_data) > 1:
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        table.wrapOn(doc, page_width, page_height)
        x = (page_width - table_width) / 2
        y_table = current_y - row_height * len(table_data)
        table.drawOn(doc, x, y_table)

        doc.setFont("Times-Roman", 12)
        doc.drawString(50, y_table - 25, f"Nombre d'enregistrements : {len(stagiaires)}")

    generer_pdf_avec_pied_de_page(doc, username)
    doc.showPage()
    doc.save()

    return response

