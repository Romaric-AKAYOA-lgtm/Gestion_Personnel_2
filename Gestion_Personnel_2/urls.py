from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path("home", views.home_view, name='home'),
    path('Activation/', include('Activation.urls')),
    path('fonction/', include('fonction.urls')),
    path('specialite/', include('specialite.urls')),
    path('OrganizationalUnit/', include('OrganizationalUnit.urls')),
        path('Employee/', include('Employe.urls')),
      path('unite/', include('unite.urls')),
    path('typeConge/', include('TypeConge.urls')),
    path('administration/', include('administration.urls')),
     path('', include('connection.urls')),  # Assurez-vous que c'est bien 'connecton'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
