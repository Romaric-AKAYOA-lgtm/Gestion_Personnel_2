from django.urls import path
from . import views

app_name = "affectation"

urlpatterns = [
    # Liste de toutes les affectations
    path('', views.lister_affectations, name='list'),

    # Détail d'une affectation spécifique
    path('<int:id>/detail/', views.detail_affectation, name='detail'),

    # Formulaire d'ajout d'une affectation
    path('ajouter/', views.ajouter_affectation, name='create'),

    # Formulaire de modification d'une affectation
    path('<int:id>/modifier/', views.modifier_affectation, name='update'),

    # Suppression d'une affectation
    path('<int:id>/supprimer/', views.supprimer_affectation, name='delete'),

    # Recherche des affectations
    path('recherche/', views.rechercher_affectations, name='search'),
]
