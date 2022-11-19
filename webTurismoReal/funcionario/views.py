from audioop import reverse
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.template.loader import get_template
from home.models import DetalleDpto, Reserva, ImagenDepartamento
from django.contrib import messages
from funcionario import urls
from funcionario.forms import *

#PDF related
from io import BytesIO
from xhtml2pdf import pisa

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


def funcionarioReserva_Check_PDF(request,*args, **kwargs):
    pk = kwargs.get('pk')
    reserva = get_object_or_404(Reserva,pk=pk)
    template_path = 'funcionario/reserva_Check_pdf.html'
    context = {'reserva': reserva}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estado.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('Intente nuevamente <pre>' + html + '</pre>')
    return response
