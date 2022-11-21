from urllib.parse import urlparse
from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.FuncionarioReservaListView.as_view(), name="funcionario_home"),
    path('reservas/updateCI/<int:checkin_id>/', views.checkin_update, name="checkin_update"),
    path('reservas/updateCO/<int:checkout_id>/', views.checkout_update, name="checkout_update"),
    path('reservas/save-updateCO/<int:checkout_id>/', views.save_checkout, name="save_checkout"),
]
