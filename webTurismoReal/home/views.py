from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Departamento, DetalleDpto, Reserva, Comuna
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as lg
from django.views.generic import CreateView
from .forms import Registro
from .models import Usuario
from django.contrib import messages
import datetime, re

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
                messages.warning(request, "Lo sentimos no hay departamentos disponibles")
            data = {
                'detalles_dpto': detalle_dpto,
                'all_location': all_location,
                'flag': True,
            }
            response = render(request, 'home/home.html', data)

        except Exception as e:
            messages.error(request, "No hay departamentos disponibles en la zona seleccionada")
            response = render(request, 'home/home.html', {'all_location': all_location})

    else:
        data = {'all_location': all_location}
        response = render(request, 'home/home.html', data)
    return HttpResponse(response)


def login(request):     
    if request.user.is_authenticated:
        return redirect ('home')     
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuarios = authenticate(username=username, password=password)       
        if usuarios: 
            lg(request,usuarios)
            messages.success(request, f'Bienvenido {usuarios.username}')
            return redirect("home")       
        else:
            messages.error(request, f'Datos incorrectos')
    return render(request, 'users/login.html',{})


def salir(request):
    logout(request)
    messages.success(request,'Sesion finalizada')
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