from django.shortcuts import render, get_object_or_404, redirect
from connection.views import get_connected_user
from .models import Fonction
from .forms import FonctionForm
 
def fonction_list(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    fonction = Fonction.objects.all().order_by('designation')
    return render(request, 'fonction/fonction_list.html', {
        'fonction': fonction,
        'username': username
    })

def fonction_create(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    if request.method == "POST":
        form = FonctionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fonction:fonction')
    else:
        form = FonctionForm()
    return render(request, 'fonction/fonction_form.html', {
        'form': form,
        'username': username
    })

def fonction_detail(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    fonction = get_object_or_404(Fonction, id=id)
    return render(request, 'fonction/fonction_detail.html', {
        'directeur': fonction,
        'username': username
    })

def modifier_fonction(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    fonction = get_object_or_404(Fonction, id=id)

    if request.method == "POST":
        form = FonctionForm(request.POST, instance=fonction)
        if form.is_valid():
            form.save()
            return redirect('fonction:fonction')
    else:
        form = FonctionForm(instance=fonction)

    return render(request, 'fonction/fonction_form_edit.html', {
        'form': form,
        'fonction': fonction,
        'username': username
    })

def supprimer_fonction(request, id):
    fonction = get_object_or_404(Fonction, id=id)
    fonction.delete()
    return redirect('fonction:fonction')

def fonction_search(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    query = request.GET.get('query', '').strip()
    fonction = Fonction.objects.all().order_by('designation')
    
    if query:
        fonction = fonction.filter(designation__icontains=query)

    return render(request, 'fonction/search.html', {
        'fonction': fonction,
        'query': query,
        'username': username
    })
