from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from Activation.models import Activation
from .models import Specialite
from .forms import  SpecialiteForm
 
def specialite_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    specialite =Specialite.objects.all().order_by('designation')
    return render(request, 'specialite/specialite_list.html', {
        'specialite': specialite})

def specialite_create(request):
    if request.method == "POST":
        form = SpecialiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialite:specialite')
    else:
        form = SpecialiteForm()
    return render(request, 'specialite/specialite_form.html', {'form': form })

def specialite_detail(request, id):
    specialite = get_object_or_404(Specialite, id=id)
    return render(request, 'specialite/specialite_detail.html', {'specialite': specialite,})

def modifier_specialite(request, id):
    specialite = get_object_or_404(Specialite, id=id)

    if request.method == "POST":
        form =SpecialiteForm(request.POST, instance=specialite)
        if form.is_valid():
            form.save()
            return redirect('specialite:specialite')  # Redirigez vers la liste des fonction après la sauvegarde
    else:
        form =SpecialiteForm (instance=specialite)  # Remplir le formulaire avec les données existantes

    return render(request, 'specialitE/specialite_form_edit.html', {'form': form, 'specialite':specialite})

def supprimer_specialite(request, id):
    specialite = get_object_or_404(Specialite , id=id)
    specialite.delete()
    return redirect('specialite:specialite')


def specialite_search(request):
    query = request.GET.get('query', '').strip()  # Récupérer la requête de recherche et supprimer les espaces inutiles
    
    # Récupérer les spécialités en fonction de la recherche
    specialites = Specialite.objects.all().order_by('designation')
    
    if query:
        specialites = specialites.filter(designation__icontains=query)

    return render(request, 'specialite/search.html', {
        'specialites': specialites,
        'query': query,
    })
