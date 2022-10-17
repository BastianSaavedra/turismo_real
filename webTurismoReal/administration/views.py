from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from home.models import Departamento, DetalleDpto, Reserva
from datetime import datetime

# Create your views here.

def sumatoria():
    data = []

    try:
        year = datetime.now().year
        for m in range(1, 13):
            total = Reserva.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(r=Coalesce(Sum('total_reserva'), 0)).get('r')
            data.append(float(total))
    except:
        pass
    return data



def administration_dashboard(request):

    # if request.user.is_staff == False:
    #     return HttpResponse('Acceso Denegado')

    detalles_dptos = DetalleDpto.objects.all()
    total_departamentos = len(detalles_dptos)
    departamentos_disponibles = len(
        DetalleDpto.objects.all().filter(status = '1')
    )
    departamentos_no_disponibles = len(
        DetalleDpto.objects.all().filter(status = '2')
    )
    reservas = len(Reserva.objects.all())
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
            'detalles_dptos': detalles_dptos,
            'total_departamentos': total_departamentos,
            'disponibles': departamentos_disponibles,
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

