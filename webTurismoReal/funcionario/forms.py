from django import forms
from home.models import Reserva

class FormularioCheckIn(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = (
         # 'guest',
         # 'booking_id',
         'status_estadia',
         'mensaje_check_in'
        )
        labels = {
            # 'guest':'Cliente',
            # 'booking_id':'Codigo Reserva',
            'status_estadia':'Estado',
            'mensaje_check_in': 'Comentarios'
        }
        widgets = {
            # 'guest':forms.Select(
            #     attrs = {
            #         'class':'form-control ',
            #         'id': 'Cliente',
            #         'name':'guest',
            #     }
            # ),
            # 'booking_id':forms.TextInput(
            #     attrs={
            #         'class':'form-control',
            #         'placeholder': 'ID_Reserva',
            #         'id': 'identificador',
            #         'name':'id_reserva',
            #     }
            # ),
            
            'status_estadia':forms.Select(
                attrs = {
                    'class':'form-control bg-white',
                    'placeholder': 'Estado de reserva',
                    'id': 'status',
                    'name':'estado_estadia'
                }
            ),
            
            'mensaje_check_in': forms.Textarea(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': 'Realiza un comentario sobre la reserva',
                    'id': 'check-in',
                    'name':'comentario_checkIn'
                }  
            ),
        }



class FormularioCheckOut(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = (
            'guest',
            'booking_id',
            'mensaje_check_out',
            'costo_multa'
        )
        labels = {
            'guest':'Cliente',
            'booking_id':'Codigo Reserva',
            'mensaje_check_out': 'Comentarios',
            'costo_multa':'Monto a multar'
        }
        widgets = {
             'guest':forms.Select(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Cliente',
                    'id': 'Cliente',
                    'name':'guest',
                    'disabled': 'true',
                }
            ),
             
            'booking_id':forms.TextInput(
                attrs={
                    'class':'form-control bg-white',
                    'placeholder': 'ID_Reserva',
                    'id': 'identificador',
                    'name':'id_reserva',
                    'disabled': 'true',
                }
            ),
            
            'mensaje_check_out': forms.Textarea(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': 'Realiza un comentario sobre la reserva',
                    'id': 'check-in',
                    'name':'comentario_checkIn'
                }  
            ),
            
            'costo_multa': forms.NumberInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': '$',
                    'id': 'multa',
                    'name':'costo_multa'
                }  
            ),
        }


    
