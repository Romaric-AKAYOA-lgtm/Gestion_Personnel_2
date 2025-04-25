from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from Activation.models import Activation
from TypeConge.form import CLTypeCongeForm
from TypeConge.models import CLTypeConge
from connection.views import get_connected_user


def typeconge_list(request):

    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')
    types = CLTypeConge.objects.all().order_by('designation')
    return render(request, 'typeconge/typeconge_list.html', {
        'username': username,
        'types': types
    })


def typeconge_create(request):
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

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
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

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
    username = get_connected_user(request)
    if not username:
        return redirect('connection:login')

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
