from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError
from django.db.models import Q

from connection.views import get_connected_user
from .models import CLParcoursStagiaire
from .forms import CLParcoursStagiaireForm


# 1. Liste des parcours stagiaires
def lister_parcours(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        parcours = CLParcoursStagiaire.objects.all().order_by('-date_debut')
        return render(request, 'ParcoursStagiaaire/lister_parcours.html', {
            'parcours': parcours,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage des parcours : {e}")


def ajouter_parcours(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    if request.method == "POST":
        form = CLParcoursStagiaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parcours_stagiaire:list')
    else:
        form = CLParcoursStagiaireForm()

    return render(request, 'ParcoursStagiaaire/ajouter_parcours.html', {
        'form': form,
        'username': username
    })



# 3. Détail d’un parcours
def detail_parcours(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        parcours = get_object_or_404(CLParcoursStagiaire, id=id)
        return render(request, 'ParcoursStagiaaire/detail_parcours.html', {
            'parcours': parcours,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de l'affichage du détail : {e}")


# 4. Modifier un parcours
def modifier_parcours(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    parcours = get_object_or_404(CLParcoursStagiaire, id=id)
    form = CLParcoursStagiaireForm(request.POST or None, instance=parcours)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                return redirect('parcours_stagiaire:list')
            except IntegrityError:
                form.add_error(None, "Erreur d'intégrité lors de la modification.")

    return render(request, 'ParcoursStagiaaire/modifier_parcours.html', {
        'form': form,
        'parcours': parcours,
        'username': username
    })


# 5. Supprimer un parcours
def supprimer_parcours(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        parcours = get_object_or_404(CLParcoursStagiaire, id=id)
        parcours.delete()
        return redirect('parcours_stagiaire:list')
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la suppression : {e}")


# 6. Rechercher des parcoursfrom django.db.models import Q
def rechercher_parcours(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        query = request.GET.get('query', '').strip()
        if query:
            parcours = CLParcoursStagiaire.objects.filter(
                Q(evaluation__icontains=query) |
                Q(commentaire__icontains=query) |
                Q(stagiaire__tnm__icontains=query) |        # ici tnm et non nom
                Q(responsable__tnm__icontains=query)       # idem ici
            ).order_by('-date_debut')
        else:
            parcours = CLParcoursStagiaire.objects.all().order_by('-date_debut')

        return render(request, 'ParcoursStagiaaire/lister_parcours.html', {
            'parcours': parcours,
            'username': username,
            'query': query
        })
    except Exception as e:
        return HttpResponseServerError(f"Erreur serveur lors de la recherche : {e}")
