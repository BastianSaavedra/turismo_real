from unicodedata import name
from django.urls import path
import administration.views as views

urlpatterns = [
    path('dashboard/', views.administration_dashboard, name="administration_dashboard"),
    # Departamento's Views
    path('departamento/list/', views.AdministracionDepartamentoListView.as_view(), name="administration_departamento"),
    path('departamento/add/', views.AdministracionDepartamentoCreateView.as_view(), name="administration_departamento_create"),
    path('departamento/edit/delete-img/<int:pk>/', views.delete_imagen, name='administration_delete_imagen'),
    path('departamento/edit/<int:pk>/', views.AdministracionDepartamentoUpdateView.as_view(), name="administration_departamento_update"),

    # Reserva's Views
    path('reserva/list/', views.AdministracionReservaListView.as_view(), name="administration_reserva"),
    path('reserva/add/', views.AdministracionReservaCreateView.as_view(), name="administration_reserva_create"),
    path('reserva/edit/<int:pk>/', views.AdministracionReservaUpdateView.as_view(), name="administration_reserva_update"),

    # Conductor Views
    path('conductor/list/', views.AdministracionConductorListView.as_view(), name="administration_conductor"),
    path('conductor/add/', views.AdministracionConductorCreateView.as_view(), name="administration_conductor_create"),
    path('conductor/edit/<int:pk>/', views.AdministracionConductorUpdateView.as_view(), name="administration_conductor_update")

       
]
