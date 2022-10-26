from audioop import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from home.models import DetalleDpto, Reserva, ImagenDepartamento
from funcionario import urls
from funcionario.forms import *

# Create your views here.

class FuncionarioReservaListView(ListView):
    model = Reserva
    template_name = 'funcionario/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Reservas'
        context['object_list'] = Reserva.objects.all()
        return context

class FuncionarioReservaUpdateView1(UpdateView):
    model = Reserva
    form_class = FormularioCheckIn
    template_name = 'funcionario/reserva_CI.html'
    success_url = reverse_lazy('funcionario_home')
    
    def get_context_data(self, **kwargs):
        context = super(FuncionarioReservaUpdateView1, self).get_context_data(**kwargs)
        return context
    
    
class FuncionarioReservaUpdateView2(UpdateView):
    model = Reserva
    form_class = FormularioCheckOut
    template_name = 'funcionario/reserva_CO.html'
    success_url = reverse_lazy('funcionario_home')
    def get_context_data(self, **kwargs):
        context = super(FuncionarioReservaUpdateView2, self).get_context_data(**kwargs)
        return context
