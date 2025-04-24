from django.shortcuts import render, redirect, get_object_or_404

from unite.models import Unite
from .models import OrganizationalUnit
from .forms import OrganizationalUnitForm
from connection.views import get_connected_user
# Vue pour afficher toutes les unités organisationnelles
def liste_OrganizationalUnit(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    organizational_units = OrganizationalUnit.objects.all().order_by('name') # Changement de nom ici
    return render(request, 'OrganizationalUnit/liste_unites.html', {
       'username' : username, 'organizational_units': organizational_units})

def ajouter_OrganizationalUnit(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    form = OrganizationalUnitForm()

    # Récupération des données associées pour les unités et les unités organisationnelles
    unite_dict = {unite.id: unite.designation for unite in Unite.objects.all().order_by('designation')}
    organizational_units_dict = {org_unit.id: org_unit.name for org_unit in OrganizationalUnit.objects.all().order_by('name')}
    
    if request.method == 'POST':
        form = OrganizationalUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('OrganizationalUnit:list')

    return render(request, 'OrganizationalUnit/ajouter_unite.html', {
        'username': username, 
        'form': form,
        'unite_dict': unite_dict,
        'organizational_units_dict': organizational_units_dict,
    })
def modifier_OrganizationalUnit(request, id):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    unite = get_object_or_404(OrganizationalUnit, id=id)
    unite_dict = {unite.id: unite.designation for unite in Unite.objects.all().order_by('designation')}
    organizational_units_dict = {org_unit.id: org_unit.name for org_unit in OrganizationalUnit.objects.all().order_by('name')}
    
    if request.method == 'POST':
        form = OrganizationalUnitForm(request.POST, instance=unite)
        if form.is_valid():
            form.save()
            return redirect('OrganizationalUnit:list')  # Rediriger vers la liste après modification
    else:
        form = OrganizationalUnitForm(instance=unite)  # Initialisation du formulaire avec les données de l'unité

    return render(request, 'OrganizationalUnit/modifier_unite.html', {
        'username': username, 
        'form': form, 
        'unite': unite,
        'unite_dict': unite_dict,
        'organizational_units_dict': organizational_units_dict,
    })

# Vue pour supprimer une unité organisationnelle
def supprimer_OrganizationalUnit(request, id):
    organizational_unit = get_object_or_404(OrganizationalUnit, id=id)  # Changement de nom ici
    organizational_unit.delete()
    return redirect('OrganizationalUnit:list')
from django.db.models import Q

def search_organizational_units(request):
    username = get_connected_user(request)

    if not username:
        return redirect('connection:login')

    query_value = request.GET.get('query', '').strip()
    filter_criteria = request.GET.get('filter', '')

    # Initialisation de la variable
    organizational_units = []

    if query_value and filter_criteria:
        filters = Q()
        if filter_criteria == "name":
            filters = Q(name__icontains=query_value)
        elif filter_criteria == "designation":
            filters = Q(designation__icontains=query_value)
        elif filter_criteria == "unite":
            filters = Q(unite__name__icontains=query_value)
        elif filter_criteria == "parent":
            filters = Q(parent__name__icontains=query_value)

        try:
            organizational_units = OrganizationalUnit.objects.filter(filters).order_by('name')
        except Exception as e:
            organizational_units = []
            print(f"Erreur lors de la récupération des unités organisationnelles : {e}")
    else:
        # Si la valeur de recherche est vide, afficher toutes les unités organisationnelles
        try:
            organizational_units = OrganizationalUnit.objects.all().order_by('name')
        except Exception as e:
            organizational_units = []
            print(f"Erreur lors de la récupération des unités organisationnelles : {e}")

    return render(request, 'OrganizationalUnit/liste_unites.html', {
        'username': username,
        'organizational_units': organizational_units,  # Utilisation de organizational_units
        'query': query_value,  # Passage du critère de recherche
        'filter': filter_criteria,  # Passage du critère de filtre
    })
