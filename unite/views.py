from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from connection.views import get_connected_user

from .models import Unite
from .forms import UniteForm
 
def unite_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    unite = Unite.objects.all().order_by('designation')
    return render(request, 'unite/unite_list.html', {
       'username':username, 'unite': unite})

def unite_create(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    if request.method == "POST":
        form = UniteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unite:unite')
    else:
        form = UniteForm()
    return render(request, 'unite/unite_form.html', {'form': form, 'username':username})


def modifier_unite(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    unite = get_object_or_404(Unite, id=id)

    if request.method == "POST":
        form =UniteForm(request.POST, instance=unite)
        if form.is_valid():
            form.save()
            return redirect('unite:unite')  # Redirigez vers la liste des fonction après la sauvegarde
    else:
        form = UniteForm (instance=unite)  # Remplir le formulaire avec les données existantes

    return render(request, 'unite/unite_form_edit.html', {'form': form, 'unite': unite, 'username':username})

def supprimer_unite(request, id):
    unite = get_object_or_404(Unite , id=id)
    unite.delete()
    return redirect('unite:unite')

def unite_search(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (username, first_name, email, etc.)
    
    # Initialisation de la queryset avec toutes les unités
    unites = Unite.objects.all().order_by('designation')

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'designation':
            unites = unites.filter(designation__icontains=query)  # Filtrer par désignation
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        unites = unites.filter(designation__icontains=query)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not unites:
        unites = None  # Pas d'unités trouvées

    return render(request, 'unite/search.html', {
        'unites': unites,
        'username': username,
        'query': query,
        'criteres': critere,
    })
