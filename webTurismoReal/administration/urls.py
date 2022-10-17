from unicodedata import name
from django.urls import path
import administration.views as views

urlpatterns = [
    path('dashboard/', views.administration_dashboard, name="administration_dashboard"),
    # path('user/arriendo-dpto/arriendo', arriendo_confirmacion, name="arriendo_dpto"),

    
]
