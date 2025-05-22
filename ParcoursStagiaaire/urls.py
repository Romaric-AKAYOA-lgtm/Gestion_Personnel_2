from django.urls import path
from . import views, views_print

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

    # PDF d’un stagiaire spécifique
    path('<int:parcours_id>/pdf/', views_print.generate_parcours_pdf, name='pdf_parcours'),

    # PDF de la liste des stagiaires (groupés par le plus récent)
    path('pdf/liste/', views_print.generate_parcours_annee_pdf , name='pdf_liste_stagiaires'),
]
