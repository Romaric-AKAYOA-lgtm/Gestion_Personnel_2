# views.py dans ton app Mutation
from django.shortcuts import render, get_object_or_404, redirect
from connection.views import get_connected_user
from mutation.forms import CLMutationForm
from .models import CLMutation

# 1. Lister toutes les mutations
def lister_mutations(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    mutations = CLMutation.objects.all().order_by('-date_debut')
    return render(request, 'Mutation/lister_mutations.html', {    'username': username, 'mutations': mutations})

# 2. Créer une nouvelle mutation
def creer_mutation(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    if request.method == 'POST':
        form = CLMutationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Mutation:list')
    else:
        form = CLMutationForm()
    return render(request, 'Mutation/creer_mutation.html', {   'username': username, 'form': form})

# 3. Voir les détails d'une mutation
def detail_mutation(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    mutation = get_object_or_404(CLMutation, id=id)
    return render(request, 'Mutation/detail_mutation.html', {    'username': username, 'mutation': mutation})

# 4. Modifier une mutation existante
def modifier_mutation(request, id):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    mutation = get_object_or_404(CLMutation, id=id)

    if request.method == 'POST':
        form = CLMutationForm(request.POST, instance=mutation)
        if form.is_valid():
            form.save()
            return redirect('Mutation:list')
    else:
        form = CLMutationForm(instance=mutation)

    return render(request, 'Mutation/modifier_mutation.html', {
        'username': username,
        'form': form,
        'mutation': mutation
    })

# 5. Supprimer une mutation
def supprimer_mutation(request, id):
    mutation = get_object_or_404(CLMutation, id=id)
    mutation.delete()
    return redirect('Mutation:list')


from django.db.models import Q

# Assure-toi d'importer aussi get_connected_user s'il est défini ailleurs

def rechercher_mutations(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

    criteres = request.GET.get('criteres')
    query = request.GET.get('query')
    mutations = CLMutation.objects.all().order_by('-date_debut')

    if criteres and query:
        if criteres == 'employe':
            mutations = mutations.filter(
                Q(employe__tnm__icontains=query) | Q(employe__tpm__icontains=query)
            )
        elif criteres == 'organizational_unit':
            mutations = mutations.filter(organizational_unit__name__icontains=query)
        elif criteres == 'function':
            mutations = mutations.filter(function__designation__icontains=query)
        elif criteres == 'responsable':
            mutations = mutations.filter(
                Q(responsable__tnm__icontains=query) | Q(responsable__tpm__icontains=query)
            )

    return render(request, 'Mutation/lister_mutations.html', {
        'username': username,
        'mutations': mutations,
        'criteres': criteres,
        'query': query,
    })
