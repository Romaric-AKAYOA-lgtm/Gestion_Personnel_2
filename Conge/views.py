from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError

from connection.views import get_connected_user
from .models import CLConge
from .forms import CLCongeForm

# 1. Liste des congés
def lister_conges(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        conges = CLConge.objects.all().order_by('-date_debut_previsionnel')
        return render(request, 'conge/lister_conges.html', {'conges': conges,    "username": username, })
    except Exception as e:
        # Capturer toute exception et renvoyer une page d'erreur générale
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage des congés : {e}")

def ajouter_conge(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    if request.method == 'POST':
        form = CLCongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conge:list')
    else:
        form = CLCongeForm()

    return render(request, 'conge/ajouter_conge.html', {
        'form': form,
        'username': username
    })

# 3. Détails d'un congé
def detail_conge(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        conge = get_object_or_404(CLConge, id=id)
        return render(request, 'conge/detail_conge.html', {'conge': conge,        "username": username, })
    except Exception as e:
        # Capturer les erreurs comme si l'objet n'existe pas
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage du congé : {e}")

# 4. Modifier un congé
def modifier_conge(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        conge = get_object_or_404(CLConge, id=id)
        if request.method == 'POST':
            form = CLCongeForm(request.POST, instance=conge)
            if form.is_valid():
                form.save()
                return redirect('conge:list')
            else:
                # Si le formulaire est invalide, afficher les erreurs
                return render(request, 'conge/modifier_conge.html', {'form': form, 'conge': conge,     "username": username,  'errors': form.errors})
        else:
            form = CLCongeForm(instance=conge)
        return render(request, 'conge/modifier_conge.html', {'form': form, 'conge': conge,      "username": username, })
    except IntegrityError as e:
        # Capturer des erreurs d'intégrité (par exemple, violation de contraintes de base de données)
        return render(request, 'conge/modifier_conge.html', {'form': form, 'conge': conge,   "username": username,  'errors': ['Erreur d\'intégrité des données.']})
    except Exception as e:
        # Capturer toute autre erreur
        return HttpResponseServerError(f"Erreur serveur lors de la modification du congé : {e}")

# 5. Supprimer un congé
def supprimer_conge(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        conge = get_object_or_404(CLConge, id=id)
        conge.delete()
        return redirect('conge:list')
    except Exception as e:
        # Gestion des erreurs liées à la suppression
        return HttpResponseServerError(f"Erreur serveur lors de la suppression du congé : {e}")

from django.db.models import Q

def rechercher_conges(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        query = request.GET.get('query', '').strip()

        if query:
            conges = CLConge.objects.filter(
                Q(employe__tnm__icontains=query) |
                Q(employe__tpm__icontains=query) |
                Q(typeconge__designation__icontains=query)
            ).order_by('-date_debut_previsionnel')
        else:
            conges = CLConge.objects.all().order_by('-date_debut_previsionnel')

        return render(request, 'conge/lister_conges.html', {
            "username": username, 
            'conges': conges,
            'query': query
        })

    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la recherche de congés : {e}")
