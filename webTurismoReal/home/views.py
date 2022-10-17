from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import total_ordering
from .models import Departamento, DetalleDpto, Reserva, Comuna, Region
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
    # all_location = Comuna.objects.values_list('nombre', 'id').distinct().order_by()
    # all_locations = Departamento.objects.values_list('comuna__nombre', 'comuna__region__nombre', 'id').distinct().order_by()
    all_locations = Departamento.objects.values_list('comuna__nombre', 'comuna__region__nombre', 'id').distinct().order_by()
    # comunas = Departamento.objects.values_list('comuna__nombre', 'comuna__img', 'id').distinct().order_by()
    comunas = Departamento.objects.all()
    if request.method == "POST":
        try:
            departamento = Departamento.objects.all().get(
                id=int(request.POST['search_location'])
            )
            rr = []

            for each_reservation in Reserva.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.detalle_dpto.id)

            detalle_dpto = DetalleDpto.objects.all().filter(
                departamento=departamento, 
                capacidad__gte = int(request.POST['capacidad'])
            ).exclude(id__in=rr)
  
                    
            if len(detalle_dpto) > 0:
                messages.success(request, "Departamentos Disponibles")
            elif len(detalle_dpto) == 0:
                messages.warning(request, "Lo siento no hay departamentos disponibles")
            data = {
                'detalles_dpto': detalle_dpto,
                'all_locations': all_locations,
                'comunas': comunas,
                'flag': True,
            }
            response = render(request, 'home/home.html', data)

        except Exception as e:
            messages.error(request, "No hay departamentos disponibles en la zona que elegiste")
            response = render(request, 'home/home.html', {
                'all_locations': all_locations,
                'comunas': comunas,
            })

    else:
        # data = {'all_location': all_location}
        data = {
            'all_locations': all_locations,
            'comunas': comunas,
        }
        response = render(request, 'home/home.html', data)
    return HttpResponse(response)

# @login_required(login_url='/user')
def home_reserva_confirmacion(request, id):
    # detalle_dpto = DetalleDpto.objects.all().get(
    #     id = int(request.GET['dptoid'])
    # )

    

    detalle_dpto = DetalleDpto.objects.all().filter(id=id).get()


    return HttpResponse(
        render(
            request,
            'user/bookdpto.html', {'detalle_dpto': detalle_dpto}
        )
    )


# @login_required(login_url='/user')
def home_reserva(request):
    if request.method == "POST":

        detalle_dpto_id = request.POST['detalledptoid']

        detalle_dpto = DetalleDpto.objects.all().get(id=detalle_dpto_id)

            
        for each_reservation in Reserva.objects.all().filter(detalle_dpto = detalle_dpto):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_in']):
                pass
            else:
                messages.warning(request, "Lo siento este departamento no esta disponible para reservar")
                return redirect("home_inicio")

        current_user = request.user
        total_person = int( request.POST['capacidad'])
        booking_id = str(detalle_dpto_id) + str(datetime.datetime.now())

        reservation = Reserva()
        detalle_dpto_object = DetalleDpto.objects.all().get(id=detalle_dpto_id)
        detalle_dpto_object.status = '2'

        user_object = User.objects.all().get(username=current_user)
        
        reservation.guest = user_object
        reservation.detalle_dpto = detalle_dpto_object
        person = total_person

        # check_in = datetime.datetime.strptime( request.POST['check_in'], '%d-%m-%Y')
        # check_in_format = datetime.datetime.strftime(check_in, '%Y-%m-%d') 
        # reservation.check_in = check_in_format

        
        # check_out = datetime.datetime.strptime( request.POST['check_out'], '%d-%m-%Y')
        # check_out_format = datetime.datetime.strftime(check_out, '%Y-%m-%d')

        # reservation.check_out = check_out_format

        # Guardado de fechas en bbdd
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']


        # obtengo las fechas para poder tener la cantidad de dias que hay entre ellas
        startDate = datetime.datetime.strptime(reservation.check_in, "%Y-%m-%d")
        endDate = datetime.datetime.strptime(reservation.check_out, "%Y-%m-%d")

        # restamos la fecha de termino con la de inicio
        diffdays = endDate - startDate

        # obtenemos la cantidad de dias
        days = diffdays.days

        # obtenemos el precio total multiplicando los dias con el precio del dpto por noche
        total_precio_reserva = days * reservation.detalle_dpto.precio
        
        # guardamos los dias en la bbdd
        reservation.cant_dias_reserva =  days

        # guardamos el total de la reserva en la bbdd
        reservation.total_reserva = total_precio_reserva

        # guardamos el id de la reserva creada en la variable booking_id
        reservation.booking_id = booking_id

        reservation.save()

        messages.success(request, "Felicidades! Tu reserva fue ingresada Exitosamente!")

        return redirect("home_inicio")
    else:
        return HttpResponse('Acceso Denegado')

def home_reservas_usuario(request):
    if request.user.is_authenticated == False:
        return redirect("home_inicio")
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id = {request.user.id}")
    reservas = Reserva.objects.all().filter(guest=user)
    if not reservas:
        messages.warning(request, "Aún no tienes reservas")
    return HttpResponse(
        render(
            request,
            'user/reservas_usuario.html',
            { 'reservas': reservas }
        )
    )
