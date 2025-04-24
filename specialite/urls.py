from django.urls import path
from . import views

app_name = 'specialite'

urlpatterns = [
    # Page d'accueil ou liste des spécialités
    path('', views.specialite_list, name='specialite'),

    # Création d'une nouvelle spécialité
    path('creer/', views.specialite_create, name='creer'),

    # Détail d'une spécialité
    path('<int:id>/', views.specialite_detail, name='information'),

    # Modification d'une spécialité
    path('<int:id>/modifier/', views.modifier_specialite, name='modifier'),

    # Suppression d'une spécialité
    path('<int:id>/supprimer/', views.supprimer_specialite , name='supprimer'),

    # Recherche de spécialités
    path('recherche/', views.specialite_search, name='recherche'),
]
