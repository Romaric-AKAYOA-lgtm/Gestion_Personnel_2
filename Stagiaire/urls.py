from django.urls import path
from . import views

app_name = "stagiaire"

urlpatterns = [
    # Liste de tous les stagiaires
    path('', views.lister_stagiaires, name='list'),

    # Détail d'un stagiaire spécifique
    path('<int:id>/detail/', views.detail_stagiaire, name='detail'),

    # Formulaire d'ajout de stagiaire
    path('ajouter/', views.ajouter_stagiaire, name='create'),

    # Formulaire de modification d'un stagiaire
    path('<int:id>/modifier/', views.modifier_stagiaire, name='update'),

    # Suppression d'un stagiaire
    path('<int:id>/supprimer/', views.supprimer_stagiaire, name='delete'),

    # Recherche des stagiaires
    path('recherche/', views.rechercher_stagiaires, name='search'),
]
