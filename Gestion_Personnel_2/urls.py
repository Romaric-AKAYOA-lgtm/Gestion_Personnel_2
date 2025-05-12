from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views, views_print

urlpatterns = [
    path('admin/', admin.site.urls),
     path("home", views.home_view, name='home'),
      path('entete/', views_print.generer_entete_pdf, name='entete_pdf'),
       path('footer/', views_print.generer_pdf_avec_pied_de_page, name='footer_pdf'),
        path('complet/', views_print.generer_pdf_complet, name='complet_pdf'),
    path('Activation/', include('Activation.urls')),
    path('fonction/', include('fonction.urls')),
    path('specialite/', include('specialite.urls')),
    path('OrganizationalUnit/', include('OrganizationalUnit.urls')),
    path('Employee/', include('Employe.urls')),
      path('conge/', include('Conge.urls')),
        path('mission/', include('mission.urls')),
        path('Mutation/', include('mutation.urls')),
      path('affectation/', include('Affectation.urls')),
      path('stagiaire/', include('Stagiaire.urls')),
        path('parcours_stagiaire/', include('ParcoursStagiaaire.urls')),
         path('employe_mission/', include('EmployeMission.urls')),
      path('unite/', include('unite.urls')),
    path('typeConge/', include('TypeConge.urls')),
    path('administration/', include('administration.urls')),
     path('', include('connection.urls')),  # Assurez-vous que c'est bien 'connecton'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
