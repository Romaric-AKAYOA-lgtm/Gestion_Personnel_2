from django.urls import path
from . import views

app_name = "parcours_stagiaire"

urlpatterns = [
    # Liste de tous les parcours stagiaires
    path('', views.lister_parcours, name='list'),

    # Détail d’un parcours spécifique
    path('<int:id>/detail/', views.detail_parcours, name='detail'),

    # Formulaire d’ajout d’un parcours
    path('ajouter/', views.ajouter_parcours, name='create'),

    # Formulaire de modification d’un parcours
    path('<int:id>/modifier/', views.modifier_parcours, name='update'),

    # Suppression d’un parcours
    path('<int:id>/supprimer/', views.supprimer_parcours, name='delete'),

    # Recherche de parcours
    path('recherche/', views.rechercher_parcours, name='search'),
]
