from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.db import IntegrityError
from django.db.models import Q

from connection.views import get_connected_user
from .models import CLAffectation
from .forms import CLAffectationForm

# 1. List all affectations
def lister_affectations(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    try:
        affectations = CLAffectation.objects.all()
        return render(request, 'Affectation/lister_affectations.html', {
            'affectations': affectations,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Server error while listing affectations: {e}")

# 2. Detail view of a single affectation
def detail_affectation(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        affectation = get_object_or_404(CLAffectation, id=id)
        return render(request, 'Affectation/detail_affectation.html', {
            'affectation': affectation,
            'username': username
        })
    except Exception as e:
        return HttpResponseServerError(f"Server error while showing detail: {e}")

# 3. Add a new affectation
def ajouter_affectation(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    
    if request.method == 'POST':
        form = CLAffectationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affectation:list')
    else:
        form = CLAffectationForm()
    
    return render(request, 'Affectation/ajouter_affectation.html', {
        'form': form,
        'username': username
    })

# 4. Update an existing affectation
def modifier_affectation(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    affectation = get_object_or_404(CLAffectation, id=id)

    try:
        if request.method == 'POST':
            form = CLAffectationForm(request.POST, instance=affectation)
            if form.is_valid():
                form.save()
                return redirect('affectation:list')
            else:
                return render(request, 'Affectation/modifier_affectation.html', {
                    'form': form,
                    'affectation': affectation,
                    'username': username,
                    'errors': form.errors
                })
        else:
            form = CLAffectationForm(instance=affectation)

        return render(request, 'Affectation/modifier_affectation.html', {
            'form': form,
            'affectation': affectation,
            'username': username
        })
    except IntegrityError:
        return render(request, 'Affectation/modifier_affectation.html', {
            'form': form,
            'affectation': affectation,
            'username': username,
            'errors': ["Data integrity error."]
        })
    except Exception as e:
        return HttpResponseServerError(f"Server error while updating affectation: {e}")

# 5. Delete an affectation
def supprimer_affectation(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        affectation = get_object_or_404(CLAffectation, id=id)
        affectation.delete()
        return redirect('affectation:list')
    except Exception as e:
        return HttpResponseServerError(f"Server error while deleting affectation: {e}")

# 6. Search affectations
def rechercher_affectations(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    try:
        query = request.GET.get('query', '').strip()

        if query:
            affectations = CLAffectation.objects.filter(
                Q(employe__tnm__icontains=query) |
                Q(employe__tpm__icontains=query) |
                Q(organisme_affecte__icontains=query) |
                Q(lieu_affectation__icontains=query) |
                Q(statut__icontains=query)
            )
        else:
            affectations = CLAffectation.objects.all()

        return render(request, 'Affectation/lister_affectations.html', {
            'affectations': affectations,
            'username': username,
            'query': query
        })

    except Exception as e:
        return HttpResponseServerError(f"Server error during search: {e}")
