from django.shortcuts import redirect, render
from django.shortcuts import render
from connection.views import get_connected_user


def home_view(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('connection:login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Contexte avec les données à passer au template
    context = {
           'username':username, 
    }

    # Rendre la vue avec le template 'home.html' et passer les données au contexte
    return render(request, "home.html", context)
