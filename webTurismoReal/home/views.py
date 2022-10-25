from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
# <<<<<<< HEAD
from django.utils.functional import total_ordering
from .models import Departamento, DetalleDpto, Reserva, Comuna, Region
# =======
from django.urls import reverse_lazy
from .models import Departamento, DetalleDpto, Reserva, Comuna
# >>>>>>> origin/branch_SebastianZuniga
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as lg
from django.views.generic import CreateView
from .forms import Registro
from .models import Usuario
from django.contrib import messages
import datetime


def home_inicio(request):
    all_locations = Departamento.objects.values_list('comuna__nombre', 'comuna__region__nombre', 'id').distinct().order_by().filter(detalle__status = '1')
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
                capacidad__gte = int(request.POST['capacidad']),
                status = '1'
            ).exclude(id__in=rr)
  
                    
            if len(detalle_dpto) > 0:
                messages.success(request, "Departamentos Disponibles")
            elif len(detalle_dpto) == 0:
                messages.warning(request, "Lo sentimos no hay departamentos disponibles")
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
            messages.info(request, "Debes completar los campos para obtener resultados")
            response = render(request, 'home/home.html', {'all_locations': all_locations})

    else:
        data = {
            'all_locations': all_locations,
            'comunas': comunas,
        }
        response = render(request, 'home/home.html', data)
    return HttpResponse(response)

# @login_required(login_url='/user')
def home_reserva_confirmacion(request, id):
    
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

        user_object = Usuario.objects.all().get(username=current_user)
        
        reservation.guest = user_object
        reservation.detalle_dpto = detalle_dpto_object
        person = total_person


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

        messages.success(request, "Felicidades!", extra_tags="Tu reserva fue ingresada Exitosamente!")

        return redirect("home_inicio")
    else:
        return HttpResponse('Acceso Denegado')

def home_reservas_usuario(request):
    if request.user.is_authenticated == False:
        return redirect("home_inicio")
    user = Usuario.objects.all().get(id=request.user.id)
    print(f"request user id = {request.user.id}")
    reservas = Reserva.objects.all().filter(guest=user, status = '1')
    if not reservas:
        messages.warning(request, "Aún no tienes reservas", extra_tags="Debes reservar un departamento para poder visualizar")
    return HttpResponse(
        render(
            request,
            'user/reservas_usuario.html',
            { 'reservas': reservas }
        )
    )

@require_http_methods(['POST'])
def cancelar_reserva(request, id):
    Reserva.objects.filter(id=id).update(status="2")
    messages.success(
        request,
        "Reserva Cancelada",
        extra_tags="Tu reserva ha sido cancelada"
    )
    return redirect("home_reservas_usuario")
    
    

def login(request):     
    if request.user.is_authenticated:
        return redirect ('home')     
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuarios = authenticate(username=username, password=password)
        # if usuarios.is_admin:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("administration_dashboard")
        # elif usuarios.is_staff:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("")
        # elif usuarios.is_funcionario:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("")
        # elif usuarios.is_admin == False:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("home_inicio")
        # else:
        #     messages.error(request, 'Datos Incorrectos')

        if usuarios: 
            lg(request,usuarios)
            messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
            return redirect("home")       
        else:
            messages.error(request, f'Datos incorrectos', extra_tags='Completa nuevamente los campos')
    return render(request, 'users/login.html',{})


def salir(request):
    logout(request)
    messages.success(request,'Sesion finalizada', extra_tags=f'Hasta pronto amigo!')
    return redirect(login)


class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = Registro
    template_name = 'users/registro.html'
    success_url = reverse_lazy('home/home.html')
    

    
    def post(self,request,*args,**kwargs):      
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                correo = form.cleaned_data.get('correo'),
                username = form.cleaned_data.get('username'),
                nombre = form.cleaned_data.get('nombre'),
                ap_paterno = form.cleaned_data.get('ap_paterno'),
                ap_materno = form.cleaned_data.get('ap_materno'),
                rut = form.cleaned_data.get('rut'),
                dv = form.cleaned_data.get('dv'),
                telefono = form.cleaned_data.get('telefono')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            
            if nuevo_usuario:
                lg(request, nuevo_usuario, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Bienvenido {form.print_user()}')
                return redirect('home')
            #return redirect('home')
        else:
            return render(request,self.template_name,{'form':form})
# >>>>>>> origin/branch_SebastianZuniga
