from django.urls import path
from . import views, views_print

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

    path('pdf/affectation/<int:affectation_id>/', views_print.generate_affectation_pdf, name='pdf_affectation'),
    path('pdf/affectations_annee/', views_print.generate_affectations_annee_pdf, name='pdf_affectations_annee'),
]