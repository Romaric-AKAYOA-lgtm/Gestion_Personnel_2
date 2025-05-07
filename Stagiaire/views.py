from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError
from django.db.models import Q

from connection.views import get_connected_user
from .models import CLStagiaire
from .forms import ClStagiaireForm

# 1. Liste des stagiaires
def lister_stagiaires(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        stagiaires = CLStagiaire.objects.all()
        return render(request, 'stagiaire/lister_stagiaires.html', {'stagiaires': stagiaires, "username": username})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage des stagiaires : {e}")

# 2. Ajouter un stagiaire
def ajouter_stagiaire(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    if request.method == 'POST':
        form = ClStagiaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stagiaire:list')
    else:
        form = ClStagiaireForm()

    return render(request, 'stagiaire/ajouter_stagiaire.html', {
        'form': form,
        'username': username
    })

# 3. Détails d’un stagiaire
def detail_stagiaire(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        stagiaire = get_object_or_404(CLStagiaire, id=id)
        return render(request, 'stagiaire/detail_stagiaire.html', {'stagiaire': stagiaire, "username": username})
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage du stagiaire : {e}")

# 4. Modifier un stagiaire
def modifier_stagiaire(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        stagiaire = get_object_or_404(CLStagiaire, id=id)
        if request.method == 'POST':
            form = ClStagiaireForm(request.POST, request.FILES, instance=stagiaire)
            if form.is_valid():
                form.save()
                return redirect('stagiaire:list')
            else:
                return render(request, 'stagiaire/modifier_stagiaire.html', {
                    'form': form,
                    'stagiaire': stagiaire,
                    'username': username,
                    'errors': form.errors
                })
        else:
            form = ClStagiaireForm(instance=stagiaire)
        return render(request, 'stagiaire/modifier_stagiaire.html', {'form': form, 'stagiaire': stagiaire, 'username': username})
    except IntegrityError:
        return render(request, 'stagiaire/modifier_stagiaire.html', {
            'form': form,
            'stagiaire': stagiaire,
            'username': username,
            'errors': ["Erreur d'intégrité des données."]
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la modification du stagiaire : {e}")

# 5. Supprimer un stagiaire
def supprimer_stagiaire(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        stagiaire = get_object_or_404(CLStagiaire, id=id)
        stagiaire.delete()
        return redirect('stagiaire:list')
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la suppression du stagiaire : {e}")

# 6. Rechercher des stagiaires
def rechercher_stagiaires(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        query = request.GET.get('query', '').strip()

        if query:
            stagiaires = CLStagiaire.objects.filter(
                Q(tnm__icontains=query) |
                Q(tpm__icontains=query) |
                Q(theme__icontains=query) |
                Q(filiere__icontains=query)
            )
        else:
            stagiaires = CLStagiaire.objects.all()

        return render(request, 'stagiaire/lister_stagiaires.html', {
            'stagiaires': stagiaires,
            'username': username,
            'query': query
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la recherche de stagiaires : {e}")
