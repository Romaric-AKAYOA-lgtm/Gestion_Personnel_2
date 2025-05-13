# urls.py dans ton app Mutation

from django.urls import path
from . import views, views_print

app_name = 'Mutation'  # très important pour utiliser {% url 'Mutation:create' %} par exemple

urlpatterns = [
    # 1. Lister toutes les mutations
    path('', views.lister_mutations, name='list'),

    # 2. Créer une nouvelle mutation
    path('create/', views.creer_mutation, name='create'),
    #  Ajouter la route pour la recherche
    path('search/', views.rechercher_mutations, name='search'),
    # 3. Détail d'une mutation
    path('<int:id>/detail/', views.detail_mutation, name='detail'),

    # 4. Modifier une mutation existante
    path('<int:id>/update/', views.modifier_mutation, name='update'),

    # 5. Supprimer une mutation
    path('<int:id>/delete/', views.supprimer_mutation, name='delete'),
     path('mutation/pdf/<int:mutation_id>/', views_print.generate_mutation_pdf, name='mutation_pdf'),
    path('mutations/pdf/annssee/', views_print.generate_mutations_annee_pdf, name='mutations_annee_pdf'),
]
