from django.urls import path
from . import views

app_name = 'typeconge'

urlpatterns = [
    path('', views.typeconge_list, name='typeconge'),
    path('creer/', views.typeconge_create, name='creer'),
    path('<int:id>/modifier/', views.modifier_typeconge, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_typeconge, name='supprimer'),
    path('recherche/', views.typeconge_search, name='recherche'),
]
