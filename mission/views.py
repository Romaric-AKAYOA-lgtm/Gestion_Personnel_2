from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError
from django.db.models import Q

from connection.views import get_connected_user
from .models import CLMission
from .forms import CLMissionForm

# 1. Liste des missions
def lister_missions(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        missions = CLMission.objects.all().order_by('-date_debut')
        return render(request, 'mission/lister_missions.html', {'missions': missions, "username": username})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage des missions : {e}")

# 2. Ajouter une mission
def ajouter_mission(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        if request.method == 'POST':
            form = CLMissionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('mission:list')
            else:
                return render(request, 'mission/ajouter_mission.html', {'form': form, "username": username, 'errors': form.errors})
        else:
            form = CLMissionForm()
        return render(request, 'mission/ajouter_mission.html', {'form': form, "username": username})
    except IntegrityError:
        return render(request, 'mission/ajouter_mission.html', {'form': form, "username": username, 'errors': ['Erreur d\'intégrité des données.']})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'ajout de la mission : {e}")

# 3. Détail d'une mission
def detail_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        mission = get_object_or_404(CLMission, id=id)
        return render(request, 'mission/detail_mission.html', {'mission': mission, "username": username})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage de la mission : {e}")

# 4. Modifier une mission
def modifier_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        mission = get_object_or_404(CLMission, id=id)
        if request.method == 'POST':
            form = CLMissionForm(request.POST, instance=mission)
            if form.is_valid():
                form.save()
                return redirect('mission:list')
            else:
                return render(request, 'mission/modifier_mission.html', {'form': form, 'mission': mission, "username": username, 'errors': form.errors})
        else:
            form = CLMissionForm(instance=mission)
        return render(request, 'mission/modifier_mission.html', {'form': form, 'mission': mission, "username": username})
    except IntegrityError:
        return render(request, 'mission/modifier_mission.html', {'form': form, 'mission': mission, "username": username, 'errors': ['Erreur d\'intégrité des données.']})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la modification de la mission : {e}")

# 5. Supprimer une mission
def supprimer_mission(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        mission = get_object_or_404(CLMission, id=id)
        mission.delete()
        return redirect('mission:list')
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la suppression de la mission : {e}")

# 6. Rechercher des missions
def rechercher_missions(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        query = request.GET.get('query', '').strip()

        if query:
            missions = CLMission.objects.filter(
                Q(objet__icontains=query) |
                Q(description__icontains=query) |
                Q(lieu_mission__icontains=query) |
                Q(organisme__icontains=query)
            ).order_by('-date_debut')
        else:
            missions = CLMission.objects.all().order_by('-date_debut')

        return render(request, 'mission/lister_missions.html', {
            "username": username,
            'missions': missions,
            'query': query
        })

    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la recherche des missions : {e}")
