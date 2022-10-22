from unicodedata import name
from django.urls import path
import administration.views as views

urlpatterns = [
    path('dashboard/', views.administration_dashboard, name="administration_dashboard"),
    path('departamento/list/', views.AdministracionDepartamentoListView.as_view(), name="administration_departamento"),
    path('departamento/create/', views.AdministracionDepartamentoCreateView.as_view(), name="administration_departamento_create"),


    path('departamento/edit/delete-img/<int:pk>/', views.delete_imagen, name='administration_delete_imagen'),


    # path('departamento/create/', views.administration_create, name="administration_departamento_create"),
    path('departamento/edit/<int:pk>/', views.AdministracionDepartamentoUpdateView.as_view(), name="administration_departamento_update"),
    # path('departamento/edit/<int:id>/', views.administration_update , name="administration_departamento_update"),
    path('reservas/', views.AdministracionReservaListView.as_view(), name="administration_reserva")
    
    # path('user/arriendo-dpto/arriendo', arriendo_confirmacion, name="arriendo_dpto"),

    
]
