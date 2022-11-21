import os
from secrets import token_urlsafe
from typing import List
from django.contrib.admin.options import reverse
from django.db.models.functions import Coalesce
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from home.models import (
    Comuna, Departamento, DetalleDpto, Reserva, ImagenDepartamento,
    Conductor, Transporte, Modelo, Marca, Tour, Usuario, DetalleTP
    )
from .forms import (
    DepartamentoForm, DetalleFormSet, ImagenFormSet, DetalleFormSetUpdate, ImagenFormSetUpdate,
    DepartamentoStatusForm ,ReservaForm, ConductorForm, TransporteForm, ModeloForm, MarcaForm,
    TransporteStatusForm, TourForm, ReservaStatusForm, DetalleTPForm, ConductorStatusForm
    )

from datetime import datetime
from django.db import transaction
from webTurismoReal import settings

# Reportes
from xhtml2pdf import pisa


# Create your views here.

def sumatoria():
    data = []

    try:
        year = datetime.now().year
        for m in range(1, 13):
            total = Reserva.objects.filter(date_joined__year=year, date_joined__month=m, status="1").aggregate(r=Coalesce(Sum('total_reserva'), 0)).get('r')
            data.append(float(total))
    except:
        pass
    return data 

def total_reserva():
    total = Reserva.objects.filter(Q(status='1') | Q(status='3')).aggregate(r=Coalesce(Sum('total_reserva'), 0)).get('r')
    return total

def administration_dashboard(request):

    # if request.user.is_staff == False
    #     return HttpResponse('Acceso Denegado')

    detalles_dptos = DetalleDpto.objects.all()
    departamentos_disponibles = len(
        DetalleDpto.objects.all().filter(status = '1')
    )
    departamentos_en_mantencion = len(
        DetalleDpto.objects.all().filter(status = '2')
    )
    departamentos_no_disponibles = len(
        DetalleDpto.objects.all().filter(status = '3')
    )
    total_departamentos = len(detalles_dptos)

    reservas = len(Reserva.objects.all().filter(status = '1'))
    reservas_canceladas = len(
        Reserva.objects.all().filter(status = '2')
    )

    departamentos = Departamento.objects.values_list('direccion', 'id').distinct().order_by()



    # Cantidad por regiones
    aisen = len(
        Departamento.objects.all().filter(comuna__region__nombre="Aisén del General Carlos Ibáñez del Campo")
    )

    antofagasta = len(
        Departamento.objects.all().filter(comuna__region__nombre="Antofagasta")
    )

    arica = len(
        Departamento.objects.all().filter(comuna__region__nombre="Arica y Parinacota")
    )

    atacama = len(
        Departamento.objects.all().filter(comuna__region__nombre="Atacama")
    )

    biobio = len(
        Departamento.objects.all().filter(comuna__region__nombre="BioBío")
    )

    coquimbo = len(
        Departamento.objects.all().filter(comuna__region__nombre="Coquimbo")
    )

    araucania = len(
        Departamento.objects.all().filter(comuna__region__nombre="La Araucanía")
    )

    libertador = len(
        Departamento.objects.all().filter(comuna__region__nombre="Libertador General Bernardo O'Higgins")
    )

    lagos = len(
        Departamento.objects.all().filter(comuna__region__nombre="Los Lagos")
    )

    rios = len(
        Departamento.objects.all().filter(comuna__region__nombre="Los Ríos")
    )

    magallanes = len(
        Departamento.objects.all().filter(comuna__region__nombre="Magallanes y de la Antártica Chilena")
    )

    maule = len(
        Departamento.objects.all().filter(comuna__region__nombre="Maule")
    )

    metropolitana = len(
        Departamento.objects.all().filter(comuna__region__nombre="Metropolitana de Santiago")
    )

    nuble = len(
        Departamento.objects.all().filter(comuna__region__nombre="Ñuble")
    )
    
    tarapaca = len(
        Departamento.objects.all().filter(comuna__region__nombre="Tarapacá")
    )
    
    valparaiso = len(
        Departamento.objects.all().filter(comuna__region__nombre="Valparaiso")
    )

    #Ventas por annio
    suma_total = sumatoria()

    response = render(
        request,
        'administration/dashboard.html',
        {
            'departamentos': departamentos,
            'reservas': reservas,
            'reservas_canceladas': reservas_canceladas,
            'detalles_dptos': detalles_dptos,
            'total_departamentos': total_departamentos,
            'disponibles': departamentos_disponibles,
            'mantencion': departamentos_en_mantencion,
            'no_disponibles': departamentos_no_disponibles,

            # regiones
            'aisen': aisen,
            'antofagasta': antofagasta,
            'arica': arica,
            'atacama': atacama,
            'biobio': biobio,
            'coquimbo': coquimbo,
            'araucania': araucania,
            'libertador': libertador,
            'lagos': lagos,
            'rios': rios,
            'magallanes': magallanes,
            'maule': maule,
            'metropolitana': metropolitana,
            'nuble': nuble,
            'tarapaca': tarapaca,
            'valparaiso': valparaiso,

            'suma_total': suma_total,
   
        }
    )

    return HttpResponse(response)

# Departamento Views
class AdministracionDepartamentoListView(ListView):
    model = DetalleDpto
    template_name = 'administration/interfaces/departamentos/departamentos.html'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Departamentos'
        context['object_list'] = DetalleDpto.objects.all()
        context['create_url'] = reverse_lazy('administration_departamento_create')
        return context


class DepartamentoInline():
    form_class = DepartamentoForm
    model = Departamento
    template_name = "administration/interfaces/departamentos/departamento_create_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('administration_departamento')

    def formset_detalles_valid(self, formset):
        detalles = formset.save(commit=False)
        for detalle in detalles:
            detalle.departamento = self.object
            detalle.save()

    def formset_imagenes_valid(self, formset):
        imagenes = formset.save(commit=False)
        for imagen in imagenes:
            imagen.departamento = self.object
            imagen.save()


class AdministracionDepartamentoCreateView(DepartamentoInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(AdministracionDepartamentoCreateView, self).get_context_data(**kwargs)
        ctx['named_formset'] = self.get_named_formsets()
        ctx['title'] = 'Agregando Nuevo Departamento'
        ctx['icon'] = 'fa-solid fa-plus'
        return ctx


    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'detalles': DetalleFormSet(prefix='detalles'),
                'imagenes': ImagenFormSet(prefix='imagenes'),
            }
        else:
            return {
                'detalles': DetalleFormSet(
                    self.request.POST or None, 
                    self.request.FILES or None, 
                    prefix = 'detalles'
                ),
                'imagenes': ImagenFormSet(
                    self.request.POST or None, 
                    self.request.FILES or None, 
                    prefix = 'imagenes'
                ),
            }


class AdministracionDepartamentoUpdateView(DepartamentoInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(AdministracionDepartamentoUpdateView, self).get_context_data(**kwargs)
        context['named_formset'] = self.get_named_formsets()
        context['title'] = 'Editando Departamento'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context

    def get_named_formsets(self):
        return {
            'detalles': DetalleFormSetUpdate(
                self.request.POST or None,
                self.request.FILES or None,
                instance = self.object,
                prefix = 'detalles'
            ),
            'imagenes': ImagenFormSetUpdate(
                self.request.POST or None,
                self.request.FILES or None,
                instance = self.object,
                prefix = 'imagenes'
            )
        }


class AdministracionDptoStatusUpdateView(UpdateView):
    model = DetalleDpto
    form_class = DepartamentoStatusForm
    success_url = reverse_lazy('administration_departamento')
    template_name = 'administration/interfaces/departamentos/departamento_status_edit.html'

    def get_context_data(self, **kwargs):
        context = super(AdministracionDptoStatusUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Estado del Departamento'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context


def delete_imagen(request, pk):
    try:
        imagen = ImagenDepartamento.objects.get(id=pk)
    except ImagenDepartamento.DoesNotExist:
        messages.success(
            request,
            'Archivo No Existe'
        )
        return redirect('administration_update', pk=imagen.departamento.id)

    imagen.delete()
    messages.success(
        request,
        'Imagen eliminada exitosamente'
    )

    return redirect('administration_departamento_update', pk=imagen.departamento.id)


# Reservas Views
class AdministracionReservaListView(ListView):
    model = Reserva
    template_name = 'administration/interfaces/reservas/reservas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Reservas'
        context['total'] = total_reserva() 
        context['object_list'] = Reserva.objects.all()
        return context
            

class AdministracionReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'administration/interfaces/reservas/reserva_create_update.html'

    def get_context_data(self, **kwargs):
        context = super(AdministracionReservaCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nueva Reserva'
        context['icon'] = 'fa-solid fa-plus'
        return context 


class AdministracionReservaUpdateView(UpdateView):
    model = Reserva
    form_class = ReservaForm
    success_url = reverse_lazy('administration_reserva')
    template_name = 'administration/interfaces/reservas/reserva_create_update.html'

    def get_context_data(self, **kwargs):
        context = super(AdministracionReservaUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Reserva'
        context['icon'] = 'fa-solid fa-pen-to-square'
        context['object_list'] = Reserva.objects.all()
        return context


class AdministracionReservaDetailView(DetailView):
    model = Reserva
    template_name = 'administration/interfaces/reservas/reserva_detail.html'
    context_object_name = 'obj'


class ReservaDetailPdfView(View):

    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(
                'media Uri must start with %s or %s' % (sUrl, mUrl)
            )
        return path

 
    def get(self, request, *args, **kwargs):
        now = datetime.now()
        try:
            template = get_template('administration/interfaces/reservas/reserva_detail_pdf.html')
            context = {
                'obj': Reserva.objects.get(pk=self.kwargs['pk']),
                'icon': '{}{}'.format(settings.STATIC_ROOT, 'img/logo_2.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report-{}.pdf"'.format(now)
            pisaStatus = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=self.link_callback

            )

            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administration_reserva'))



class AdministracionReservaStatusEdit(UpdateView):
    model = Reserva
    form_class = ReservaStatusForm
    template_name = 'administration/interfaces/reservas/reserva_status_edit.html'
    success_url = reverse_lazy('administration_reserva')
    
    def get_context_data(self, **kwargs):
        context = super(AdministracionReservaStatusEdit, self).get_context_data(**kwargs)
        context['title'] = 'Editando Estado de la Reserva'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context


## Cliente Views
class AdministracionClienteListView(ListView):
    model = Usuario
    template_name = 'administration/interfaces/clientes/clientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de clientes'
        context['object_list'] = Usuario.objects.all().filter(
            usuario_cliente__gte = True, 
            usuario_superAdministrador = False
        )
        return context


class AdministracionClienteReservasListView(ListView):
    queryset = Reserva.objects.all()
    template_name = 'administration/interfaces/clientes/reservas_por_cliente.html'
    context_object_name = 'reservas'
    success_url = reverse_lazy('administration_cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Reservas del cliente'
        context['cliente'] = Usuario.objects.filter(id=self.request.resolver_match.kwargs['pk'])
        context['icon'] = 'far fa-address-book'
        return context

    def get_queryset(self):
        return Reserva.objects.filter(guest=self.request.resolver_match.kwargs['pk'])



# Conductor Views
class AdministracionConductorListView(ListView):
    model = Conductor
    template_name = 'administration/interfaces/conductores/conductores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Conductores'
        context['object_list'] = Conductor.objects.all()
        context['create_url'] = reverse_lazy('administration_condutor_create')
        return context


class AdministracionConductorCreateView(CreateView):
    model = Conductor
    form_class = ConductorForm
    template_name = 'administration/interfaces/conductores/conductor_create_update.html'
    success_url = reverse_lazy('administration_conductor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregando Nuevo Conductor'
        context['icon'] = 'fa-solid fa-plus'
        return context


class AdministracionConductorUpdateView(UpdateView):
    model = Conductor
    form_class = ConductorForm
    success_url = reverse_lazy('administration_conductor')
    template_name = 'administration/interfaces/conductores/conductor_create_update.html'

    def get_context_data(self, **kwargs):
        context = super(AdministracionConductorUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Conductor'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context


class AdministracionConductorStatusEdit(UpdateView):
    model = Conductor
    form_class = ConductorStatusForm
    template_name = 'administration/interfaces/conductores/conductor_status_edit.html'
    success_url = reverse_lazy('administration_conductor')

    def get_context_data(self, **kwargs):
        context = super(AdministracionConductorStatusEdit, self).get_context_data(**kwargs)
        context['title'] = 'Editando Estado del Conductor'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context

# Transporte Views
class AdministracionTransporteListView(ListView):
    model = Transporte
    template_name = 'administration/interfaces/transportes/transportes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Transportes'
        context['object_list'] = Transporte.objects.all()
        # context['create_url'] = reverse_lazy('administration_transporte_create')
        return context


class AdministracionTransporteCreateView(CreateView):
    model = Transporte
    form_class = TransporteForm
    template_name = 'administration/interfaces/transportes/transporte_create_update.html'
    success_url = reverse_lazy('administration_transporte')

    def get_context_data(self, **kwargs):
        context = super(AdministracionTransporteCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nuevo Transporte'
        context['icon'] = 'fa-solid fa-plus'
        return context


class AdministracionTransporteUpdateView(UpdateView):
    model = Transporte
    form_class = TransporteForm
    template_name = 'administration/interfaces/transportes/transporte_create_update.html'
    success_url = reverse_lazy('administration_transporte')

    def get_context_data(self, **kwargs):
        context = super(AdministracionTransporteUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Transporte'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context


class AdministracionTransporteStatusEdit(UpdateView):
    model = Transporte
    form_class = TransporteStatusForm
    template_name = 'administration/interfaces/transportes/transporte_status_edit.html'
    success_url = reverse_lazy('administration_transporte')

    def get_context_data(self, **kwargs):
        context = super(AdministracionTransporteStatusEdit, self).get_context_data(**kwargs)
        context['title'] = 'Editando Estado del Transporte'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context



class AdministracionModeloCreateView(CreateView):
    model = Modelo
    form_class = ModeloForm
    template_name = 'administration/interfaces/transportes/modelo_create.html'
    success_url = reverse_lazy('administration_transporte_create')


    def get_context_data(self, **kwargs):
        context = super(AdministracionModeloCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nuevo Modelo del Transporte'
        context['icon'] = 'fa-solid fa-plus'
        return context


class AdministracionMarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'administration/interfaces/transportes/marca_create.html'
    success_url = reverse_lazy('administration_modelo_create')

    def get_context_data(self, **kwargs):
        context = super(AdministracionMarcaCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nueva Marca del Transporte'
        context['icon'] = 'fa-solid fa-plus'
        return context

## Servicios
class AdministracionTourListView(ListView):
    model = Tour
    template_name = 'administration/interfaces/servicios_extras/tours.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tours'
        context['object_list'] = Tour.objects.all()
        return context


class AdministracionTourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    template_name = 'administration/interfaces/servicios_extras/tour_create_update.html'
    success_url = reverse_lazy('administration_tour')

    def get_context_data(self, **kwargs):
        context = super(AdministracionTourCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nuevo Tour'
        context['icon'] = 'fa-solid fa-plus'
        return context


class AdministracionTourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    template_name = 'administration/interfaces/servicios_extras/tour_create_update.html'
    success_url = reverse_lazy('administration_tour')

    def get_context_data(self, **kwargs):
        context = super(AdministracionTourUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Tour'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context

# DetalleTP
class AdministracionDetalleTPListView(ListView):
    model = DetalleTP
    template_name = 'administration/interfaces/servicios_extras/traslados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Traslado de Clientes'
        context['object_list'] = DetalleTP.objects.all()
        return context


class AdministracionDetalleTPCreateView(CreateView):
    model = DetalleTP
    form_class = DetalleTPForm
    template_name = 'administration/interfaces/servicios_extras/traslado_create_update.html'
    success_url = reverse_lazy('administration_traslado')

    def get_context_data(self, **kwargs):
        context = super(AdministracionDetalleTPCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Agregando Nuevo Traslado'
        context['icon'] = 'fa-solid fa-plus'
        return context


class AdministracionDetalleTPUpdateView(UpdateView):
    model = DetalleTP
    form_class = DetalleTPForm
    template_name = 'administration/interfaces/servicios_extras/traslado_create_update.html'
    success_url = reverse_lazy('administration_traslado')

    def get_context_data(self, **kwargs):
        context = super(AdministracionDetalleTPUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Editando Traslado'
        context['icon'] = 'fa-solid fa-pen-to-square'
        return context





