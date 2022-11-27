from audioop import reverse
from importlib.abc import ResourceReader

from django.shortcuts import Http404, redirect, render, get_object_or_404

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
from tools import webpay


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
    reserva = Reserva.objects.get(id=checkin_id)
    return render(
        request,
        'funcionario/reserva_CI.html',
        {
            "form": FormularioCheckIn(),
            "reserva": reserva
        }
    )

def save_checkin(request, checkin_id):
    reserva = Reserva.objects.get(id=checkin_id)

    status_estadia = request.POST['status_estadia']
    comentario = request.POST['mensaje_check_in']

    reserva.status_estadia = status_estadia
    reserva.mensaje_check_in = comentario

    reserva.save()


    if status_estadia == '1':
        status = '4'
        reserva.status = status
        reserva.save()
    elif status_estadia == '2':
        status = '5'
        reserva.status = status
        reserva.save()

    return redirect('funcionario_home')

    
    



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

    print("valor multa", monto_multa)

    if int(monto_multa) == 0:
        return redirect('funcionario_home')

    id_reserva = reserva.id 
    current_user = reserva.guest.id
    valor_multa =  monto_multa
    url_webpay = 'funcionario/reservas/updateCO/pago-multa/webpay-respuesta/'

    result = webpay.crearTransaccion(
        id_reserva, current_user,
        valor_multa, url_webpay
    )
    return render(
        request,
        'funcionario/webpay.html',
        {
            'url': result['url'],
            'token': result['token']
        }

    )



def multa_webpay_respuesta(request):
    if not request.GET.get('token_ws'):
        raise Http404
    token = request.GET.get('token_ws')

    messages.success(
        request,
        "Pago autorizado",
        extra_tags = "El pago ha sido recibido"
    )
    return redirect('funcionario_home')






def funcionarioReserva_Check_PDF(request,*args, **kwargs):
    pk = kwargs.get('pk')
    reserva = get_object_or_404(Reserva,pk=pk)
    template_path = 'user/reserva_Check_pdf.html'
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
