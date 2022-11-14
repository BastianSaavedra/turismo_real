from unicodedata import name
from django.urls import path
import home.views as views

urlpatterns = [
    path('', views.home_inicio, name="home_inicio"),
    path('user/reserva-dpto/dpto=<int:id>', views.home_reserva_confirmacion, name="home_reserva_confirmacion"),
    path('user/reserva-dpto/reserva', views.home_reserva, name="home_reserva"),
    path('user/mis-reservas', views.home_reservas_usuario, name="home_reservas_usuario"),
    path('user/mis-reservas/cancelar-reserva/<id>/', views.cancelar_reserva, name="home_cancelar_reserva"),
    path('user/mis-reservas/reserva=<int:id>', views.detalle_reserva, name="detalle_reserva"),
    path('user/mis-reservas/reserva/edit/<id>/', views.agregar_servicios, name="agregar_servicios"),
    path('user/mis-reservas/cancelar-tour/<id>/', views.cancelar_tour, name="home_cancelar_tour"),
    path('user/mis-reservas/cancelar-transporte/<id>/', views.cancelar_transporte, name="home_cancelar_transporte"),
    # path('user/arriendo-dpto/arriendo', arriendo_confirmacion, name="arriendo_dpto"),
]
