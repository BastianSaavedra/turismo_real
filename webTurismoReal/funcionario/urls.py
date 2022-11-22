from urllib.parse import urlparse
from django.urls import path
from . import views
from .views import funcionarioReserva_Check_PDF

urlpatterns = [
    path('inicio/', views.FuncionarioReservaListView.as_view(), name="funcionario_home"),
    path('reservas/updateCI/<int:checkin_id>/', views.checkin_update, name="checkin_update"),
    path('reservas/updateCO/<int:checkout_id>/', views.checkout_update, name="checkout_update"),
    path('reservas/save-updateCO/<int:checkout_id>/', views.save_checkout, name="save_checkout"),

    # path('reservas/updateCI/<int:pk>/', views.FuncionarioReservaUpdateView1.as_view(), name="funcionario_CI"),
    #path('reservas/updateCI/<id>/', views.funcionarioReservaUpdateCheckIn, name="funcionario_CI"),
    # path('reservas/updateCO/<int:pk>/', views.FuncionarioReservaUpdateView2.as_view(), name="funcionario_CO"),
    path('reservas/check/pdf/<int:pk>/',views.funcionarioReserva_Check_PDF, name='detalle_reserva_pdf'),
]
