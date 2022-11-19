from urllib.parse import urlparse
from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.FuncionarioReservaListView.as_view(), name="funcionario_home"),
    path('reservas/updateCI/<int:pk>/', views.FuncionarioReservaUpdateView1.as_view(), name="funcionario_CI"),
    # path('reservas/updateCO/<int:pk>/', views.FuncionarioReservaUpdateView2.as_view(), name="funcionario_CO"),
    path('reservas/updateCO=<int:id>/', views.reserva_check_out, name="reserva_check_out"),
    path('reservas/save-checkout/<id>', views.guardar_reserva_check_out, name="guardar_reserva_check_out"),

]
