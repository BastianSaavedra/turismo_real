from audioop import reverse
from importlib.abc import ResourceReader

from django.shortcuts import redirect, render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.template.loader import get_template
from home.models import DetalleDpto, Reserva, ImagenDepartamento
from django.contrib import messages

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

def checkin_update(request, checkin_id):
    checkin = Reserva.objects.get(id=checkin_id)
    reserva = Reserva.objects.get(id=checkin_id)
    data = {
        # 'form': FormularioCheckIn(instance=checkin),
      
        'form': FormularioCheckIn(instance=checkin),
        'reserva': reserva
    }

    reserva.status = '4'
    reserva.save()
    
    if request.method == "POST":
        formulario = FormularioCheckIn(data=request.POST, instance=checkin)
    
        if formulario.is_valid():
            formulario.save()
            return redirect('funcionario_home')
        data["form"] = formulario

    
    return render(
        request,
        'funcionario/reserva_CI.html',
        data
    )



def checkout_update(request, checkout_id):
    checkout = Reserva.objects.get(id=checkout_id)
    return render(
        request,
        'funcionario/reserva_CO.html',
        {
            "checkout": checkout
        }
    )

def save_checkout(request, checkout_id):
    reserva = Reserva.objects.get(id=checkout_id)

    # guest = request.POST['cliente']
    # codigo = request.POST['codigo']
    comentario = request.POST['comentario']
    monto_multa = request.POST['montoMulta']

    reserva_status = '3'

    reserva.mensaje_check_out = comentario
    reserva.costo_multa = monto_multa

    reserva.status = reserva_status

    total_reserva = reserva.total_reserva

    suma_multa = total_reserva + int(monto_multa)

    reserva.total_reserva = suma_multa
    reserva.save()
    
    return redirect('funcionario_home')



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
