"""webTurismoReal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# <<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
# =======
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.views import logout_then_login
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
# =======
    path('', include('home.urls'), name="home.urls"),
    path('',views.home_inicio, name='home'),
    path('accounts/logout/', views.salir, name='logout'),
# >>>>>>> origin/branch_SebastianZuniga
]

if settings.DEBUG:  
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
