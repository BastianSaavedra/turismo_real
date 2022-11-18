from django.shortcuts import render
from django.http import HttpResponse
from import_export import resources
from datetime import datetime

from home.models import (
    Reserva, Usuario
    )

# Reservas's reports 

def reserva_excel_report(request):
    now = datetime.now()

    reserva_resource = resources.modelresource_factory(model=Reserva)()
    dataset = reserva_resource.export()
    response = HttpResponse(
        dataset.xls,
        content_type = 'text/xls'
    )
    response['Content-Disposition'] = 'atachment; filename="reservas-{}.xls"'.format(now)
    return response


def clientes_excel_report(request):
    now = datetime.now()

    clientes = Usuario.objects.filter(
        usuario_cliente = True,
        usuario_superAdministrador = False
    )
    clientes_resource = resources.modelresource_factory(
        model= Usuario
        )()
    dataset = clientes_resource.export()
    response = HttpResponse(
        dataset.xls,
        content_type = 'text/xls'
    )
    response['Content-Disposition'] = 'atachment; filename="clientes-{}.xls"'.format(now)
    return response
