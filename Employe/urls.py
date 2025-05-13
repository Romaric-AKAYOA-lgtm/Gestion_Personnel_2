from django.urls import path
from . import views, views_print

app_name = "Employee"

urlpatterns = [
  
    # Liste de tous les employés
    path('Employee', views.liste_employes ,name='list'),
    # Création d'un nouvel employé
    path('create/', views.ajouter_employe, name='create'),
    # Détail d'un employé
    path('<int:id>/detail/', views.detail_employe, name='detail'),

    # Modification d'un employé
    path('<int:id>/update/', views.modifier_employe, name='update'),
    # Suppression d'un employé
    path('<int:id>/delete/', views.supprimer_employe, name='delete'),
     path('employee/pdf/', views.generate_employee_pdf, name='generate_employee_pdf'),
     path('recherche/', views.employee_search, name='recherche'),  # Ajout de la route de recherche
     path('employe/pdf/<int:employe_id>/', views_print.generate_employe_pdf, name='employe_pdf'),
    path('employes/pdf/', views_print.generate_employes_pdf, name='employes_pdf'),

]
