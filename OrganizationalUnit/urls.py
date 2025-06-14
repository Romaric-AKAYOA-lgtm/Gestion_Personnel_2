from django.urls import path
from . import views, view_print

app_name = "OrganizationalUnit"

urlpatterns = [
    # Liste de toutes les unités organisationnelles
    path('', views.liste_OrganizationalUnit, name='list'),
    # Création d'une nouvelle unité organisationnelle
    path('create/', views.ajouter_OrganizationalUnit, name='create'),
    # Modification d'une unité organisationnelle
    path('<int:id>/update/', views.modifier_OrganizationalUnit, name='update'),
    # Suppression d'une unité organisationnelle
    path('<int:id>/delete/', views.supprimer_OrganizationalUnit, name='delete'),
     path('search/', views.search_organizational_units, name='search_organizational_units'),
      path('organigramme/', view_print.generate_organigramme_pdf, name='organigramme_pdf'),
]
