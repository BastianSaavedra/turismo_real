from operator import attrgetter
from django import  forms
from django.contrib.admin.options import widgets
from django.forms.models import inlineformset_factory, modelformset_factory
from home.models import Departamento, DetalleDpto, ImagenDepartamento, Reserva


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
                attrs={'class':'form-control select-search'}
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
        fields = '__all__'
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
            'status': 'Status del Departamento',
            'cant_dias_mantencion': 'Cantidad de dias en Mantencion'
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
                attrs={'class':'form-control select-search mb-4'}
            ),
            'cant_bannio': forms.NumberInput(
                attrs={'class':'form-control mb-4'}
            ),
            'dormitorio': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'cant_dormitorio': forms.NumberInput(
                attrs={'class':'form-control mb-4'}
            ),
            'estacionamiento': forms.Select(
                attrs={'class':'form-control select-search mb-4'}
            ),
            'cant_estacionamiento': forms.NumberInput(
                attrs={'class':'form-control mb-4'}
            ),
            'status': forms.Select(
                attrs={
                    'class':'form-control select-search mb-4',
                    'name': 'statusDpto',
                    'id': 'statusDpto'
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
                    'id': 'fin'
                }

            ),
            'cant_dias_mantencion': forms.NumberInput(
                attrs={
                    'class': 'form-control mb-4',
                    'id': 'dias'
                }
            ) 
        }





class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = (
            'check_in', 'check_out', 
            'detalle_dpto', 'guest', 'cant_dias_reserva',
            'total_reserva', 'status'
        )
        labels = {
            'check_in': 'Check In',
            'check_out': 'Check Out',
            'detalle_dpto': 'Departamento',
            'guest': 'Huesped',
            'cant_dias_reserva': 'Cantidad de dias de la Reserva',
            'total_reserva': 'Monto Total de la Reserva',
            'status': 'Status de la Reserva'
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
            'status': forms.Select(
                attrs={
                    'class': 'form-control',
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



