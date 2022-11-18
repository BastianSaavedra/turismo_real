from django.urls import path
from . import views

urlpatterns = [
    path('reservas-excel/', views.reserva_excel_report, name='reservas_excel_report'),
    path('clientes-excel', views.clientes_excel_report, name='clientes_excel_report')

]
