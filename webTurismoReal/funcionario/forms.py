from django import forms
from home.models import Reserva

class FormularioCheckIn(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = (
         'status_estadia',
         'mensaje_check_in'
        )
        labels = {
            'status_estadia':'Estado',
            'mensaje_check_in': 'Comentarios'
        }
        widgets = {
            'status_estadia':forms.Select(
                attrs = {
                    'class':'form-control bg-white',
                    'placeholder': 'Estado de reserva',
                    'id': 'statusEstadia',
                    'name':'statusEstadia',
                    'style':'border-radius: 10px; border-color: rgb(171, 82, 0);border-width: 1px;'
                }
            ),
            
            'mensaje_check_in': forms.Textarea(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': 'Realiza un comentario sobre la reserva',
                    'id': 'comentario',
                    'name':'comentario',
                    'style':'height:50px;border-radius: 10px; border-color: rgb(171, 82, 0);border-width: 1px; height: 150px;',
                    
                }  
            ),
        }



class FormularioCheckOut(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = (
            'mensaje_check_out',
            'costo_multa'
        )
        labels = {
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
                    'name':'comentario_checkIn',
                    'style':'height:50px;border-radius: 10px; border-color: rgb(171, 82, 0);border-width: 1px;'
                }  
            ),
            
            'costo_multa': forms.NumberInput(
                attrs = {
                    'class': 'form-control bg-white',
                    'placeholder': '$',
                    'id': 'multa',
                    'name':'costo_multa',
                    'style':'border-radius: 10px; border-color: rgb(171, 82, 0);border-width: 1px;'
                }  
            ),
        }


    
