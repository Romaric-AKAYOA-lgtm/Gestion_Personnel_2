from django.urls import path
from . import views, views_print

app_name = "mission"

urlpatterns = [
    # Liste de toutes les missions
    path('', views.lister_missions, name='list'),

    # Détail d'une mission spécifique
    path('<int:id>/detail/', views.detail_mission, name='detail'),

    # Formulaire d'ajout de mission
    path('ajouter/', views.ajouter_mission, name='create'),

    # Formulaire de modification d'une mission
    path('<int:id>/modifier/', views.modifier_mission, name='update'),

    # Suppression d'une mission
    path('<int:id>/supprimer/', views.supprimer_mission, name='delete'),

    # Recherche des missions
    path('recherche/', views.rechercher_missions, name='search'),

    # Générer le PDF pour une mission spécifique
    path('pdf/employe-mission/<int:mission_id>/', views_print.generate_mission_pdf, name='pdf_employe_mission'),

    # Générer le PDF de toutes les missions
    path('pdf/employes-missions/', views_print.generate_missions_pdf, name='pdf_employes_missions'),
]
