from django.urls import path
from . import views, views_print

app_name = "employe_mission"

urlpatterns = [
    # 🔹 Liste des liaisons employé-mission
    path('', views.lister_employe_mission, name='list'),

    # 🔹 Détail d'une liaison employé-mission
    path('<int:id>/detail/', views.detail_employe_mission, name='detail'),

    # 🔹 Ajouter une nouvelle liaison employé-mission
    path('ajouter/', views.ajouter_employe_mission, name='create'),

    # 🔹 Modifier une liaison employé-mission existante
    path('<int:id>/modifier/', views.modifier_employe_mission, name='update'),

    # 🔹 Supprimer une liaison employé-mission
    path('<int:id>/supprimer/', views.supprimer_employe_mission, name='delete'),

    # 🔹 Rechercher des liaisons employé-mission
    path('recherche/', views.rechercher_employe_missions, name='search'),
    
    path('pdf/employe-mission/<int:mission_id>/', views_print.generate_employe_mission_pdf, name='employe_mission_pdf'),
    path('pdf/employe-missions/annee/', views_print.generate_employes_missions_pdf, name='employe_missions_annee_pdf'),
]
