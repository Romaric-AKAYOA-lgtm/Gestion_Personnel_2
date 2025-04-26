from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import CLConge
from .forms import CLCongeForm

# 1. Liste des congés
def lister_conges(request):
    conges = CLConge.objects.all()
    return render(request, 'conge/lister_conges.html', {'conges': conges})

# 2. Ajouter un nouveau congé
def ajouter_conge(request):
    if request.method == 'POST':
        form = CLCongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('conge:list')
    else:
        form = CLCongeForm()
    return render(request, 'conge/ajouter_conge.html', {'form': form})

# 3. Détails d'un congé
def detail_conge(request, id):
    conge = get_object_or_404(CLConge, id=id)
    return render(request, 'conge/detail_conge.html', {'conge': conge})

# 4. Modifier un congé
def modifier_conge(request, id):
    conge = get_object_or_404(CLConge, id=id)
    if request.method == 'POST':
        form = CLCongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            return redirect('conge:detail', id=conge.id)
    else:
        form = CLCongeForm(instance=conge)
    return render(request, 'conge/modifier_conge.html', {'form': form, 'conge': conge})

# 5. Supprimer un congé
def supprimer_conge(request, id):
    conge = get_object_or_404(CLConge, id=id)
    conge.delete()
    return redirect('conge:list')

# 6. Recherche des congés
def rechercher_conges(request):
    query = request.GET.get('query', '')
    if query:
        conges = CLConge.objects.filter(employe__nom__icontains=query)  # Exemple de recherche par nom d'employé
    else:
        conges = CLConge.objects.all()
    return render(request, 'conge/lister_conges.html', {'conges': conges, 'query': query})
