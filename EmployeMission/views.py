from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError
from django.db.models import Q

from EmployeMission.form import CLEmployeMissionForm
from connection.views import get_connected_user
from .models import CLEmployeMission


# 1. Liste des affectations
def lister_employe_mission(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        affectations = CLEmployeMission.objects.all()
        return render(request, 'EmployeMission/lister_employe_mission.html', {
            'affectations': affectations,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur lors de l'affichage : {e}")


# 2. Ajout d'une affectation
def ajouter_employe_mission(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        if request.method == 'POST':
            form = CLEmployeMissionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('employe_mission:list')
        else:
            form = CLEmployeMissionForm()
        
        return render(request, 'EmployeMission/ajouter_employe_mission.html', {
            'form': form,
            'username': username
        })
    
    except IntegrityError:
        return render(request, 'EmployeMission/ajouter_employe_mission.html', {
            'form': form,
            'username': username,
            'errors': ['Erreur d\'intégrité des données.']
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur : {e}")


# 3. Détail d'une affectation
def detail_employe_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        affectation = get_object_or_404(CLEmployeMission, id=id)
        return render(request, 'EmployeMission/detail_employe_mission.html', {
            'affectation': affectation,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur : {e}")


# 4. Modification d'une affectation
def modifier_employe_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        affectation = get_object_or_404(CLEmployeMission, id=id)
        if request.method == 'POST':
            form = CLEmployeMissionForm(request.POST, instance=affectation)
            if form.is_valid():
                form.save()
                return redirect('employe_mission:list')
        else:
            form = CLEmployeMissionForm(instance=affectation)
        
        return render(request, 'EmployeMission/modifier_employe_mission.html', {
            'form': form,
            'affectation': affectation,
            'username': username
        })
    
    except IntegrityError:
        return render(request, 'EmployeMission/modifier_employe_mission.html', {
            'form': form,
            'affectation': affectation,
            'username': username,
            'errors': ['Erreur d\'intégrité des données.']
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur : {e}")


# 5. Suppression d'une affectation
def supprimer_employe_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        affectation = get_object_or_404(CLEmployeMission, id=id)
        affectation.delete()
        return redirect('employe_mission:list')
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur : {e}")


# 6. Recherche
def rechercher_employe_missions(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        query = request.GET.get('query', '').strip()
        if query:
            affectations = CLEmployeMission.objects.filter(
                Q(employe__nom__icontains=query) |
                Q(mission__objet__icontains=query)
            )
        else:
            affectations = CLEmployeMission.objects.all()
        
        return render(request, 'EmployeMission/lister_employe_mission.html', {
            'affectations': affectations,
            'username': username,
            'query': query
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur de recherche : {e}")
