from unicodedata import name
from django.urls import path
import home.views as views

urlpatterns = [
    path('', views.home_inicio, name="home_inicio"),
    path('user/reserva-dpto/dpto=<int:id>', views.home_reserva_confirmacion, name="home_reserva_confirmacion"),
    path('user/reserva-dpto/reserva', views.home_reserva, name="home_reserva"),
    path('user/mis-reservas', views.home_reservas_usuario, name="home_reservas_usuario"),
    # path('user/arriendo-dpto/arriendo', arriendo_confirmacion, name="arriendo_dpto"),

    
]
