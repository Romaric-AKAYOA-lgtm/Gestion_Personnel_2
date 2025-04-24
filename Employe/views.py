from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime
from Employe.models import CLEmploye
from .forms import ClEmployeForm
from connection.views import get_connected_user
from specialite.models import Specialite

# Liste des employés
def liste_employes(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    employes = CLEmploye.objects.all().order_by('id')
    return render(request, 'Employee/liste_employes.html', {
        'username': username, 'employes': employes
    })

# Ajouter un employé
def ajouter_employe(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    form = ClEmployeForm()
    specialite = Specialite.objects.all().order_by('designation')

    if request.method == 'POST':
        form = ClEmployeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Employee:list')
    return render(request, 'Employee/ajouter_employe.html', {
        'username': username, 'form': form,
        'specialite': specialite
    })

# Modifier un employé
def modifier_employe(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    employe = get_object_or_404(CLEmploye, id=id)
    specialite = Specialite.objects.all().order_by('designation')

    if request.method == 'POST':
        form = ClEmployeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('Employee:list')
    else:
        form = ClEmployeForm(instance=employe)
    return render(request, 'Employee/modifier_employe.html', {
        'username': username, 'form': form,
        'specialite': specialite
    })

# Supprimer un employé
def supprimer_employe(request, id):
    employe = get_object_or_404(CLEmploye, id=id)
    employe.delete()
    return render(request, 'Employee/supprimer_employe.html', {'employe': employe})

# Détail secrétaire avec mot de passe
def secretaire_detail2(request, username, password):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    secretaire = CLEmploye.objects.filter(username=username).first()
    if not secretaire or not secretaire.check_password(password):
        return render(request, "secretaire/login.html", {"error": "Nom d'utilisateur ou mot de passe incorrect."})
    if secretaire.date_fin and secretaire.date_fin < now().date():
        return render(request, "Employee/login.html", {"error": "Votre accès est expiré."})

    return render(request, "Employee/detail.html", {"secretaire": secretaire})

# Générer PDF des employés
def generate_employee_pdf(request):
    current_date = datetime.today().date()
    active_employees = CLEmploye.objects.filter(status='active')
    retired_employees = CLEmploye.objects.filter(status='retired', retirement_date__gt=current_date)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees_report.pdf"'

    buffer = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    header = Paragraph("<b>INRAP</b>", style=getSampleStyleSheet()['Title'])
    header2 = Paragraph("<b>République du Congo</b>", style=getSampleStyleSheet()['Title'])
    elements.extend([header, header2, Spacer(1, 0.25 * inch)])

    data = [['Nom', 'Prénom', 'Matricule', 'Grade', 'Spécialité', 'Date de Prise de Service', 'Date de Retraite']]
    for emp in active_employees:
        data.append([emp.tnm, emp.tpm, emp.matricule, emp.grade, emp.specialite, emp.dsb, 'Non applicable'])
    for emp in retired_employees:
        data.append([emp.tnm, emp.tpm, emp.matricule, emp.grade, emp.specialite, emp.dsb, emp.date_retraite])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    footer = Paragraph(f"Brazzaville - {datetime.now().strftime('%d/%m/%Y')}", style=getSampleStyleSheet()['Normal'])
    footer_table = Table([[footer]], colWidths=[400])
    footer_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'RIGHT')])

    elements.extend([table, Spacer(1, 0.5 * inch), footer_table])
    buffer.build(elements)
    return response

# Recherche d'employés
def employee_search(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    query = request.GET.get('query', '')
    critere = request.GET.get('criteres', '')

    employees = CLEmploye.objects.all()

    if critere and query:
        filters = {
            'username': 'username__icontains',
            'tpm': 'tpm__icontains',  # Prénom
            'tnm': 'tnm__icontains',  # Nom
            'email': 'email__icontains',
            'num_tel': 'num_tel__icontains',
            'matricule': 'matricule__icontains',
            'status': 'status__icontains'
        }
        if critere in filters:
            employees = employees.filter(**{filters[critere]: query})
    elif query:
        from django.db.models import Q
        employees = employees.filter(
            Q(username__icontains=query) |
            Q(tnm__icontains=query) |
            Q(tpm__icontains=query) |
            Q(email__icontains=query)
        )

    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    if date_debut:
        employees = employees.filter(start_date__gte=date_debut)
    if date_fin:
        employees = employees.filter(retirement_date__lte=date_fin)

    if not employees.exists():
        employees = None

    return render(request, 'employee/search.html', {
        'employees': employees,
        'username': username,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })
