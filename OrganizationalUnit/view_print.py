from django.http import HttpResponse
from django.shortcuts import redirect
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

from connection.views import get_connected_user
from .models import OrganizationalUnit
from datetime import datetime

def generate_organigramme_pdf(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="organigramme.pdf"'

    doc = canvas.Canvas(response, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)
    margin = 2 * cm

    title = f"Organigramme des Unités Organisationnelles ({datetime.now().year})"
    doc.setFont("Helvetica-Bold", 16)
    doc.drawCentredString(page_width / 2, page_height - margin, title)

    y_start = page_height - margin - 2 * cm

    # Récupérer toutes les unités
    units = OrganizationalUnit.objects.all()

    # Construire la hiérarchie en dictionnaire
    def build_tree(parent=None):
        branches = []
        for unit in units.filter(parent=parent):
            branches.append({
                'unit': unit,
                'children': build_tree(unit)
            })
        return branches

    tree = build_tree()

    # Dessiner l'organigramme récursivement
    def draw_tree(node_list, x, y, depth=0, x_offset=5*cm, y_offset=3*cm):
        for node in node_list:
            unit_name = node['unit'].name
            box_width = 4.5 * cm
            box_height = 1 * cm

            # Dessiner rectangle
            doc.rect(x - box_width / 2, y - box_height / 2, box_width, box_height, stroke=1, fill=0)
            doc.setFont("Helvetica", 8)
            doc.drawCentredString(x, y - 4, unit_name)

            # Calculer positions enfants
            child_count = len(node['children'])
            if child_count > 0:
                total_width = child_count * x_offset
                start_x = x - (total_width - x_offset) / 2

                for i, child in enumerate(node['children']):
                    child_x = start_x + i * x_offset
                    child_y = y - y_offset

                    # Dessiner ligne parent-enfant
                    doc.line(x, y - box_height / 2, child_x, child_y + box_height / 2)

                    # Récursion
                    draw_tree([child], child_x, child_y, depth + 1)

    draw_tree(tree, x=page_width / 2, y=y_start)

    doc.showPage()
    doc.save()
    return response
