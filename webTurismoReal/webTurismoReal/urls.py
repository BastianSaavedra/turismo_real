#"""webTurismoReal URL Configuration

from django.contrib import admin
from django.urls import path, include
# <<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
# =======
from django.contrib.auth.decorators import login_required
from home import views 
from home.views import *
# >>>>>>> origin/branch_SebastianZuniga

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('accounts/register', RegistrarUsuario.as_view(), name='registro'),
    path('site/admin/', admin.site.urls),
# <<<<<<< HEAD
    path('', include('home.urls'), name="home_urls"),
    path('administration/', include('administration.urls'), name="administration_urls"),
    path('funcionario/', include('funcionario.urls'), name="funcionario_urls"),
# =======
    path('',views.home_inicio, name='home'),
    path('accounts/logout/', views.salir, name='logout'),
    #path('busqueda', views.searchListView,name='search')
# >>>>>>> origin/branch_SebastianZuniga
]

if settings.DEBUG:  
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
