from django.urls import path
from . import views

app_name = "conge"

urlpatterns = [
    # Liste de tous les congés
    path('', views.lister_conges, name='list'),

    # Détail d'un congé spécifique
    path('<int:id>/detail/', views.detail_conge, name='detail'),

    # Formulaire d'ajout de congé
    path('ajouter/', views.ajouter_conge, name='create'),

    # Formulaire de modification d'un congé
    path('<int:id>/modifier/', views.modifier_conge, name='update'),

    # Suppression d'un congé
    path('<int:id>/supprimer/', views.supprimer_conge, name='delete'),

    # Recherche des congés
    path('recherche/', views.rechercher_conges, name='search'),
]
