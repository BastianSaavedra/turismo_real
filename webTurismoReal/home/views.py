from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.functional import total_ordering
from .models import Departamento, DetalleDpto, Reserva, Comuna, Region
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as lg
from django.views.generic import CreateView, UpdateView
from .forms import Registro
from .models import Usuario
from django.contrib import messages
from django.db.models import Q
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
    # Obtencion de los tours disponibles
    #all_tours = Tour.objects.values_list('nombreTour','comuna', 'id').distinct().order_by().filter(tipoTour = '1' and '2' and '3')
    # all_tours = Tour.objects.all().filter(~Q(tipoTour='0'))
    all_tours = Tour.objects.all()
    # all_transp = DetalleTP.objects.values_list('lugar_tp').filter(~Q(transporte__tipo_transporte='0'))
    # all_transp = DetalleTP.objects.all().filter(~Q(transporte__tipo_transporte='0'))
    all_transp = DetalleTP.objects.all()

    detalle_dpto = DetalleDpto.objects.all().filter(id=id).get()
    return HttpResponse(
        render(
            request,
            'user/bookdpto.html', 
            {
                'detalle_dpto': detalle_dpto,
                'all_tours':all_tours,
                'all_transp':all_transp,
            }
        )
    )


# @login_required(login_url='/user')
def home_reserva(request):
    if request.method == "POST":
        
        reservation = Reserva()
        
        
        detalle_dpto_id = request.POST['detalledptoid']
        detalle_dpto = DetalleDpto.objects.all().get(id=detalle_dpto_id)
         
        for each_reservation in Reserva.objects.all().filter(detalle_dpto = detalle_dpto):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_in']):
                pass
            else:
                messages.warning(request, "Lo sentimos este departamento no esta disponible para reservar")
                return redirect("home_inicio")

        current_user = request.user
        total_person = int( request.POST['capacidad'])
        booking_id = str(detalle_dpto_id) + str(datetime.datetime.now())

        detalle_dpto_object = DetalleDpto.objects.all().get(id=detalle_dpto_id)
        detalle_dpto_object.status = '2'
        user_object = Usuario.objects.all().get(username=current_user)
        
                
        # Guardado de cliente y detalle departamento en bbdd 
        reservation.guest = user_object
        reservation.detalle_dpto = detalle_dpto_object

        reservation.huespedes = total_person
        
        #--------------------------------- SERVICIOS ---------------------------------
        tipo_tour = request.POST['tour']
        if tipo_tour == "0":
            tipo_tour = None 
            valor_tour = 0
        else:
            tipo_tour = request.POST['tour']
            tour = Tour.objects.get(id=tipo_tour)
            valor_tour = tour.costo

        lugar_transporte = request.POST['lugar']
        if lugar_transporte == "0":
            lugar_transporte = None
            valor_transporte = 0
        else:
            lugar_transporte = request.POST['lugar']
            transp = DetalleTP.objects.get(id=lugar_transporte)
            valor_transporte = transp.costo_tp

        #--------------------------------- SERVICIOS ---------------------------------
        
        #--------------------------------------Guardado de servicios en bbdd----------------------------------------

        reservation.tour_id = tipo_tour
        reservation.detalle_tp_id = lugar_transporte
        #-----------------------------------------------------------------------------------------------------------

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
        costo_reserva = (days * reservation.detalle_dpto.precio) 
        # guardamos los dias en la bbdd
        reservation.cant_dias_reserva =  days

        reservation.costo_reserva = costo_reserva

        total_precio_reserva = costo_reserva + valor_tour + valor_transporte + reservation.costo_multa

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


@require_http_methods(['POST'])
def cancelar_tour(request, id):

    reservation = Reserva.objects.get(id=id)
    valor_total = reservation.total_reserva
    valor_tour = reservation.tour.costo

    resta_tour = valor_total - valor_tour


    Reserva.objects.filter(id=id).update(tour=None)
    Reserva.objects.filter(id=id).update(total_reserva = resta_tour)
    messages.success(
        request,
        "Tour Cancelado",
        extra_tags="El servicio ha sido eliminado de tu reserva"
    )
    return redirect("home_reservas_usuario")
    

@require_http_methods(['POST'])
def cancelar_transporte(request, id):
    
    reservation = Reserva.objects.get(id=id)

    valor_total = reservation.total_reserva
    valor_transporte = reservation.detalle_tp.costo_tp

    resta_transporte = valor_total - valor_transporte

    Reserva.objects.filter(id=id).update(detalle_tp=None)
    Reserva.objects.filter(id=id).update(total_reserva = resta_transporte)

    messages.success(
        request,
        "Transporte Cancelado",
        extra_tags="El servicio ha sido eliminado de tu reserva"
    )
    return redirect("home_reservas_usuario")


def detalle_reserva(request, id):
    # all_tours = Tour.objects.all().filter(~Q(tipoTour='0'))
    # all_transp = DetalleTP.objects.all().filter(~Q(transporte__tipo_transporte='0'))
    all_tours = Tour.objects.all()
    all_transp = DetalleTP.objects.all()
    user = Usuario.objects.all().get(id=request.user.id)
    reservas = Reserva.objects.filter(id=id)
    return HttpResponse(
        render(
            request,
            'user/services.html',
            { 'reservas': reservas,
              'all_tours':all_tours,
              'all_transp':all_transp,}
        )
    )
  
 
@require_http_methods(['POST'])
def agregar_servicios(request,id):
    if request.method == 'POST':

        reservation = Reserva.objects.get(id=id)
        
        tipo_tour = request.POST['tour']
        if tipo_tour == "0":
            tipo_tour = None 
            valor_tour = 0
        else:
            tipo_tour = request.POST['tour']
            tour = Tour.objects.get(id=tipo_tour)
            valor_tour = tour.costo


        lugar_transporte = request.POST['lugar']
        if lugar_transporte == "0":
            lugar_transporte = None
            valor_transporte = 0
        else:
            lugar_transporte = request.POST['lugar']
            transporte = DetalleTP.objects.get(id=lugar_transporte)
            valor_transporte = transporte.costo_tp

        costo_reserva = reservation.costo_reserva 
        costo_multa = reservation.costo_multa
       

        total_precio_reserva = costo_reserva + valor_tour + valor_transporte + costo_multa
        
        Reserva.objects.filter(id=id).update(tour = tipo_tour)
        Reserva.objects.filter(id=id).update(detalle_tp = lugar_transporte)

        Reserva.objects.filter(id=id).update(total_reserva = total_precio_reserva)
        messages.success(
                        request,
                        "Reserva actualizada",
                        extra_tags="Tu reserva ha sido actualizada correctamente"
                         )

        return redirect("home_reservas_usuario")
    else:
        return HttpResponse('Acceso Denegado')


def login(request):     
    if request.user.is_authenticated:
        return redirect ('home')     
    
    elif request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # usuarios = authenticate(username=username, password=password)
        
        username = request.POST['username']
        password = request.POST['password']
        usuarios = authenticate(request, username=username, password=password)
        
                
        # if usuarios: 
        #     lg(request,usuarios)
        #     messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
        #     return redirect("home")  
        
        if usuarios: 
            
            if usuarios.is_staff:
                lg(request,usuarios)
                messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
                return redirect("home_inicio")      
            
            elif usuarios.is_cliente:
                lg(request,usuarios)
                messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
                return redirect("home_inicio")
            
            elif usuarios.is_admin:
                lg(request,usuarios)
                messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
                return redirect("/administration_dashboard") 
            
            elif usuarios.is_funcionario:
                lg(request,usuarios)
                messages.success(request, f'Bienvenido @{usuarios.username}', extra_tags='Tu sesion ha sido iniciada correctamente')
                return redirect("/funcionario/inicio.html") 
         
             
        #------------------------------------
        
        # if usuarios.is_admin:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("administration_dashboard")
        # elif usuarios.is_staff:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("")
        # elif usuarios.is_funcionario == True:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido funcionario{usuarios.username}')
        #     return redirect("funcionario_home")
        # elif usuarios.is_admin == False:
        #     lg(request, usuarios)
        #     messages.success(request, f'Bienvenido {usuarios.username}')
        #     return redirect("home_inicio")
       
        
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
                messages.success(request, f'Bienvenido {form.print_user()}', extra_tags='Tu cuenta ha sido registrada correctamente!')
                return redirect('home')
            #return redirect('home')
        else:
            return render(request,self.template_name,{'form':form})

def Reserva_Check_PDF(request,*args, **kwargs):
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