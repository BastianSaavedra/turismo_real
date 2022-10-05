from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Departamento, DetalleDpto, Reserva, Comuna
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

# def home_inicio(request):
#     return render(
#         request,
#         'home/home.html',
#         {}
#     )


def home_inicio(request):
    all_location = Comuna.objects.values_list('nombre', 'id').distinct().order_by()
    if request.method == "POST":
        try:
            print(request.POST)
            departamento = Departamento.objects.all().get(id=int(request.POST['search_location']))
            rr = []

            for each_reservation in Reserva.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.detalle_dpto.id)

            detalle_dpto = DetalleDpto.objects.all().filter(departamento=departamento, capacidad__gte = int(request.POST['capacidad'])).exclude(id__in=rr)
            if len(detalle_dpto) > 0:
                messages.success(request, "Departamentos Disponibles")
            elif len(detalle_dpto) == 0:
                messages.warning(request, "Lo siento no hay departamentos disponibles")
            data = {
                'detalles_dpto': detalle_dpto,
                'all_location': all_location,
                'flag': True,
            }
            response = render(request, 'home/home.html', data)

        except Exception as e:
            messages.error(request, "No hay departamentos disponibles en la zona que elegiste")
            response = render(request, 'home/home.html', {'all_location': all_location})

    else:
        data = {'all_location': all_location}
        response = render(request, 'home/home.html', data)
    return HttpResponse(response)
