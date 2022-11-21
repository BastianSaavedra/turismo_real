from django.urls import path
import administration.views as views

urlpatterns = [
    path('dashboard/', views.administration_dashboard, name="administration_dashboard"),
    # Departamento's Views
    path('departamento/list/', views.AdministracionDepartamentoListView.as_view(), name="administration_departamento"),
    path('departamento/add/', views.AdministracionDepartamentoCreateView.as_view(), name="administration_departamento_create"),
    path('departamento/edit/delete-img/<int:pk>/', views.delete_imagen, name='administration_delete_imagen'),
    path('departamento/edit/<int:pk>/', views.AdministracionDepartamentoUpdateView.as_view(), name="administration_departamento_update"),
    path('departamento/edit-status/<int:pk>/', views.AdministracionDptoStatusUpdateView.as_view(), name="administration_status_edit"),

    # Reserva's Views
    path('reserva/list/', views.AdministracionReservaListView.as_view(), name="administration_reserva"),
    path('reserva/add/', views.AdministracionReservaCreateView.as_view(), name="administration_reserva_create"),
    path('reserva/edit/<int:pk>/', views.AdministracionReservaUpdateView.as_view(), name="administration_reserva_update"),
    path('reserva/detail/<int:pk>/', views.AdministracionReservaDetailView.as_view(), name="administration_reserva_detail"),
    path('reserva/edit-status/<int:pk>/', views.AdministracionReservaStatusEdit.as_view(), name="administration_reserva_status_edit"),
    path('reserva/detail/pdf/<int:pk>/', views.ReservaDetailPdfView.as_view(), name="reserva_detail_pdf"),

    # Cliente Views
    path('cliente/list/', views.AdministracionClienteListView.as_view(), name="administration_cliente"),
    path('cliente/reservas-list/<int:pk>/', views.AdministracionClienteReservasListView.as_view(), name="administration_cliente_reservas"),

    # Conductor Views
    path('conductor/list/', views.AdministracionConductorListView.as_view(), name="administration_conductor"),
    path('conductor/add/', views.AdministracionConductorCreateView.as_view(), name="administration_conductor_create"),
    path('conductor/edit/<int:pk>/', views.AdministracionConductorUpdateView.as_view(), name="administration_conductor_update"),
    path('conductor/edit-status/<int:pk>/', views.AdministracionConductorStatusEdit.as_view(), name="administration_conductor_status_edit"),

    # Transporte Views
    path('transporte/list/', views.AdministracionTransporteListView.as_view(), name="administration_transporte"),
    path('transporte/add/', views.AdministracionTransporteCreateView.as_view(), name="administration_transporte_create"),
    # path('transporte/add/', views.agregar_transporte, name="administration_transporte_create"),
    path('transporte/edit/<int:pk>/', views.AdministracionTransporteUpdateView.as_view(), name="administration_transporte_update"),
    path('transporte/edit-status/<int:pk>/', views.AdministracionTransporteStatusEdit.as_view(), name="administration_transporte_status_edit"),
    path('transporte/add-modelo/', views.AdministracionModeloCreateView.as_view(), name="administration_modelo_create"),
    # path('transporte/add-modelo/update/', views.AdministracionModeloUpdateView.as_view(), name="administration_modelo_update"),
    path('transporte/add-modelo/add-marca/', views.AdministracionMarcaCreateView.as_view(), name="administration_marca_create"),

    # Tours Views
    path('tour/list/', views.AdministracionTourListView.as_view(), name="administration_tour"),
    path('tour/add/', views.AdministracionTourCreateView.as_view(), name="administration_tour_create"),
    path('tour/edit/<int:pk>/', views.AdministracionTourUpdateView.as_view(), name="administration_tour_update"),

    # Traslado Views
    path('traslado/list/', views.AdministracionDetalleTPListView.as_view(), name="administration_traslado"),
    path('traslado/add/', views.AdministracionDetalleTPCreateView.as_view(), name="administration_traslado_create"),
    path('traslado/edit/<int:pk>/', views.AdministracionDetalleTPUpdateView.as_view(), name="administration_traslado_update")




       
]
