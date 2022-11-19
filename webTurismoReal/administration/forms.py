from operator import attrgetter
from django import  forms
from django.contrib.admin.options import widgets
from django.forms.models import inlineformset_factory, modelformset_factory
from home.models import (
    Departamento, DetalleDpto, ImagenDepartamento, Reserva, Conductor,
    Transporte, Marca, Modelo, Tour, DetalleTP
    )



class DepartamentoForm(forms.ModelForm):

    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(
                attrs={'class':'form-control', 'placeholder': 'Ingresar titulo del departamento'}
            ),
            'direccion': forms.TextInput(
                attrs={'class':'form-control', 'placeholder': 'Ingresar direccion del departamento'}
            ),
            'comuna': forms.Select(
                attrs={
                    'class':'form-control', 
                    'id': 'comunas',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Agrega una descripcion del departamento'}
            )
        }


class ImagenForm(forms.ModelForm):

    class Meta:
        model = ImagenDepartamento
        fields = '__all__'
        labels = { 'imagen': 'Selecciona una imagen'}
        widgets = {
            'imagen': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )
        }
       

class DetalleForm(forms.ModelForm):

    class Meta:
        model = DetalleDpto
        fields = (
            'precio', 'capacidad', 'amoblado', 'cable', 'electronicos',
            'internet', 'aire_acondicionado', 'bodega', 'bannio',
            'cant_bannio', 'dormitorio', 'cant_dormitorio', 'estacionamiento',
            'cant_estacionamiento'
        )
        labels = {
            'departamento': 'Departamento',
            'precio': 'Precio',
            'capacidad': 'Capacidad de Huespedes',
            'amoblado': 'Amoblado',
            'cable': 'Tv Cable',
            'eletronicos': 'Artefactos Electronicos',
            'internet': 'Internet',
            'aire_acondicionado': 'Aire Acondicionado',
            'bodega': 'Bodega',
            'bannio': 'Baño',
            'cant_bannio': 'Cantidad de Baños',
            'dormitorio': 'Dormitorio',
            'cant_dormitorio': 'Cantidad de Dormitorios',
            'estacionamiento': 'Estacionamiento',
            'cant_estacionamiento': 'Cantidad de Estacionamientos',
        }
        widgets = {
            'precio': forms.NumberInput(
                attrs={'class':'form-control mb-4'}
            ),
            'capacidad': forms.NumberInput(
                attrs={'class':'form-control mb-4'}
            ),
            'amoblado': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'cable': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'electronicos': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'internet': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'aire_acondicionado': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'bodega': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'bannio': forms.Select(
                attrs={
                    'class':'form-control select-search mb-4',
                    'name': 'bannioSelect',
                    'id': 'bannioSelect'
                }
            ),
            'cant_bannio': forms.NumberInput(
                attrs={
                    'class':'form-control mb-4',
                    'id': 'cant_bannio',
                    'disabled': 'true'
                }
            ),
            'dormitorio': forms.Select(
                attrs={
                    'class': 'form-control select-search mb-4',
                    'name': 'dormitorioSelect',
                    'id': 'dormitorioSelect'
                }
            ),
            'cant_dormitorio': forms.NumberInput(
                attrs={
                    'class': 'form-control mb-4',
                    'id': 'cant_dormitorio',
                    'disabled': 'true'
                }
            ),
            'estacionamiento': forms.Select(
                attrs={
                    'class': 'form-control select-search mb-4',
                    'name': 'estacionamientoSelect',
                    'id': 'estacionamientoSelect'
                }
            ),
            'cant_estacionamiento': forms.NumberInput(
                attrs={
                    'class': 'form-control mb-4',
                    'id': 'cant_estacionamiento',
                    'disabled': 'true'
                }
            ),
        }

class DepartamentoStatusForm(forms.ModelForm):
    
    class Meta:
        model = DetalleDpto
        fields = (
            'status', 'inicio_mantencion', 'fin_mantencion',
            'cant_dias_mantencion'
        )
        widgets = {
            'status': forms.Select(
                attrs={
                    'class':'form-control select-search mb-4',
                    'name': 'statusDpto',
                    'id': 'statusDpto',
                }
            ),
            'inicio_mantencion': forms.DateInput(
                attrs={
                    'class': 'form-control bg-white',
                    'placeholder': 'Selecciona una fecha',
                    'type': 'datetime-local',
                    'id': 'inicio',
                }
            ),
            'fin_mantencion': forms.DateInput(
                attrs={
                    'class': 'form-control bg-white',
                    'placeholder': 'Selecciona una fecha',
                    'type': 'datetime-local',
                    'id': 'fin',
                }

            ),
            'cant_dias_mantencion': forms.NumberInput(
                attrs={
                    'class': 'form-control mb-4',
                    'id': 'dias',
                }
            ) 
        }


# Inline Forms Departamento
DetalleFormSet = inlineformset_factory(
    Departamento,
    DetalleDpto,
    form = DetalleForm,
    extra = 1,
    can_delete = False,
    can_delete_extra = False
)


DetalleFormSetUpdate = inlineformset_factory(
    Departamento,
    DetalleDpto,
    form = DetalleForm,
    extra = 0,
    can_delete = False,
    can_delete_extra = False
)


ImagenFormSet = inlineformset_factory(
    Departamento,
    ImagenDepartamento,
    form = ImagenForm,
    extra = 5,
    can_delete = False,
    can_delete_extra = False
)


ImagenFormSetUpdate = inlineformset_factory(
    Departamento,
    ImagenDepartamento,
    form = ImagenForm,
    extra = 0,
    can_delete = False,
    can_delete_extra = False
)


class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = (
            'check_in', 'check_out', 
            'detalle_dpto', 'guest', 'cant_dias_reserva',
            'total_reserva'
        )
        labels = {
            'check_in': 'Check In',
            'check_out': 'Check Out',
            'detalle_dpto': 'Departamento',
            'guest': 'Huesped',
            'cant_dias_reserva': 'Cantidad de dias de la Reserva',
            'total_reserva': 'Monto Total de la Reserva',
        }
        widgets = {
            'check_in': forms.DateInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': 'Selecciona una fecha',
                    'type': 'datetime-local',
                    'id': 'cin',
                }
                
            ),
            'check_out': forms.DateInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': 'Selecciona una fecha',
                    'type': 'datetime-local',
                    'id': 'cout',
                }
            ),
            # 'date_joined': forms.DateTimeInput(
            #     attrs={
            #         'class': 'form-control',
            #         'disabled': 'true',
            #     }
            # ),
            'detalle_dpto': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'guest': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'cant_dias_reserva': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'cantidad_dias',
                    'name': 'cantidad_dias',
                }
            ),
            'total_reserva': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'total_reserva',
                    'type': 'number',
                    'name': 'total_reserva',
                }
            ),
        }

class ReservaStatusForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ('status',)
        labels = {
            'status': 'Estado de Reserva'
        }
        widgets = {
            'status': forms.Select(
                attrs = {
                    'class': 'form-control select-search mb-4',
                    'name': 'statusReserva',
                    'id': 'statusReserva'

                }
            )


        }



class ConductorForm(forms.ModelForm):

    class Meta:
        model = Conductor
        fields = '__all__'
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'edad': 'Edad',
            'annio_experiencia': 'Años de Experiencia'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del conductor',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del conductor',
                }
            ),
            'edad': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                }
            ),
            'annio_experiencia': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                }
            )
        }


# Transporte Inline Form
class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = '__all__'
        labels = {
            'marca': 'Marca'
        }
        widgets = {
            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

class ModeloForm(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = '__all__'
        labels = {
            'modelo' : 'Modelo del Transporte',
            'marca' : 'Marca del Transporte'
        }
        widgets = {
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese El modelo del auto'
                }
            ),
            'marca': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'marcas'
                }
            )
        }


class TransporteForm(forms.ModelForm):

    class Meta:
        model = Transporte
        fields = (
            'patente', 'tipo_transporte', 'annio',
            'color', 'num_puertas', 'kmRecorridos',
            'conductor', 'modelo'
        )
        labels = {
            'patente': 'Patente',
            'tipo_transporte': 'Tipo de Transporte',
            'annio': 'Año del Transporte',
            'color': 'Color del Transporte',
            'num_puertas': 'Numero de Puertas del Transporte',
            'kmRecorridos': 'Kilometros Recorridos',
            'conductor': 'Conductor Asignado',
            'modelo': 'Modelo del Transporte',
        }
        widgets = {
            'patente': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Patente del Transporte'
                }
            ),
            'tipo_transporte': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'transporte'
                }
            ),
            'annio': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Color del Transporte'
                }
            ),
            'num_puertas': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'kmRecorridos': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'conductor': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'conductores'
                }
            ),
            'modelo': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'modelos'
                },
            ),
        }
        

class TransporteStatusForm(forms.ModelForm):

    class Meta:
        model = Transporte
        fields = ('status',)
        labels = {
            'status': 'Estado del Transporte'
        }
        widgets = {
            'status': forms.Select(
                attrs = {
                    'class': 'form-control select-search mb-4',
                    'name': 'statusTransporte',
                    'id': 'statusTransporte'

                }
            )
        }


class TourForm(forms.ModelForm):

    class Meta:
        model = Tour
        fields = '__all__'
        labels = {
            'tipoTour': 'Tipo de Tour',
            'nombreTour': 'Nombre del Tour',
            'horario_in': 'Horario Inicio',
            'horario_fin': 'Horario Termino',
            'costo': 'Costo del Tour',
            'comuna': 'Comuna donde se hará el Tour',
        }
        widgets = {
            'tipoTour': forms.Select(
                attrs = {
                    'class': 'form-control',
                    'id': 'tipoTour'
                }
            ),
            'nombreTour': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre del Tour'
                }
            ),
            'horario_in': forms.TimeInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'type': 'timepicker'
                }
            ),
            'horario_fin': forms.TimeInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'type': 'timepicker'
                }
            ),
            'costo': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                }
            ),
            'comuna': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Comuna donde se hará el Tour'

                }
            )

        }


class DetalleTPForm(forms.ModelForm):

    class Meta:
        model = DetalleTP
        fields = '__all__'
        labels = {
            'lugar_tp': 'Lugar Traslado',
            'horario_in': 'Horario Inicio',
            'horario_fin': 'Horario Termino',
            'costo_tp': 'Costo del Traslado',
            'transporte': 'Transporte encargado de trasladar al cliente'
        }
        widgets = {
            'lugar_tp': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Lugar Traslado'
                }
            ),
            'horario_in': forms.TimeInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'type': 'timepicker'
                }
            ),
            'horario_fin': forms.TimeInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'type': 'timepicker'
                }
            ),
            'costo_tp': forms.NumberInput(
                attrs = {
                    'class': 'form-control',
                }
            ),
            'transporte': forms.Select(
                attrs = {
                    'class': 'form-control',
                    'id': 'tipoTransporte'
                }

            )
        }



