from unicodedata import name
from django.urls import path
import administration.views as views

urlpatterns = [
    path('dashboard/', views.administration_dashboard, name="administration_dashboard"),
    path('departamentos/', views.AdministracionDepartamentoListView.as_view(), name="administration_departamento")
    
    # path('user/arriendo-dpto/arriendo', arriendo_confirmacion, name="arriendo_dpto"),

    
]
