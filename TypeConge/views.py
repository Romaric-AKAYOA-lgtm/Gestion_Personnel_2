from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from Activation.models import Activation
from TypeConge.form import CLTypeCongeForm
from TypeConge.models import CLTypeConge
from unite.views import get_username_from_session

def typeconge_list(request):

    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    types = CLTypeConge.objects.all().order_by('designation')
    return render(request, 'typeconge/typeconge_list.html', {
        'username': username,
        'types': types
    })


def typeconge_create(request):
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    if request.method == "POST":
        form = CLTypeCongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typeconge:typeconge')
    else:
        form = CLTypeCongeForm()
    
    return render(request, 'typeconge/typeconge_form.html', {
        'form': form,
        'username': username
    })

def modifier_typeconge(request, id):
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    typeconge = get_object_or_404(CLTypeConge, id=id)

    if request.method == "POST":
        form = CLTypeCongeForm(request.POST, instance=typeconge)
        if form.is_valid():
            form.save()
            return redirect('typeconge:typeconge')
    else:
        form = CLTypeCongeForm(instance=typeconge)

    return render(request, 'typeconge/typeconge_form_edit.html', {
        'form': form,
        'typeconge': typeconge,
        'username': username
    })

def supprimer_typeconge(request, id):
    typeconge = get_object_or_404(typeconge, id=id)
    typeconge.delete()
    return redirect('typeconge:typeconge')

def typeconge_search(request):
    username = get_username_from_session(request)
    if not username:
        return redirect('login')

    query = request.GET.get('query', '')
    critere = request.GET.get('criteres', '')

    types = CLTypeConge.objects.all().order_by('designation')

    if critere and query:
        if critere == 'designation':
            types = types.filter(designation__icontains=query)
    elif query:
        types = types.filter(designation__icontains=query)

    if not types.exists():
        types = None

    return render(request, 'typeconge/typeconge_list.html', {
        'types': types,
        'username': username,
        'query': query,
        'criteres': critere,
    })
