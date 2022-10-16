from datetime import MINYEAR
from django import forms
from django.forms import CharField, EmailField, TextInput
from .models import Usuario
import re

from home.models import Usuario

class Registro(forms.ModelForm):
    
    """
        Formulario de registro de un usuario dentro de la base de datos 
        
        Variables: 
            - password1: Contraseña
            - password2: Verificacion de la contraseña otorgada en el primer campo
            
    """
    
    password1 = forms.CharField(label='Contraseña',required=True, widget=forms.PasswordInput(
        {'class':'form-control',
         'placeholder':'Contraseña'
        })) 
    password2 = forms.CharField(label='Confirmar contraseña',required=True, widget=forms.PasswordInput(
        {'class':'form-control',
         'placeholder':'Confirmar contraseña'
        }))
    
    class Meta:
        model = Usuario
        fields = ('correo', 'username','nombre','ap_paterno', 'ap_materno', 
                  'rut','dv','telefono')
        widgets = {
            'correo': forms.EmailInput(
                attrs = {'class': 'form-control','placeholder':'Correo Electrónico'}),
            'nombre': forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Ingrese su Nombre'}),
            'ap_paterno' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Ingrese su apellido'}),
            'ap_materno' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Ingrese su apellido'}),
            'rut' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Ingrese su RUT'}), 
            'dv' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Dv'}),   
            'username' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Especifique un nombre de usuario'}), 
            'telefono' : forms.TextInput(
                attrs = {'class':'form-control', 'placeholder':'Digite su numero telefonico'})
        }


    def clean_username(self): 
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username = username).exists():
            raise forms.ValidationError('Usuario ya existente')
        return username

    def clean_email(self): 
        correo = self.cleaned_data.get('email')
        if Usuario.objects.filter(email = correo).exists():
            raise forms.ValidationError('Correo ya vinculado')
        return correo
    
    """def clean_rut(self):
        
        Validacion de rut
        
        Metodo que valida que el rut ingresado se encuentre en el rango numerico 0-9.
        
        Excepciones:
            -ValidationError = Mensaje de error que aparece cuando se ingresan caracteres no coincidentes
        
        if not re.match("^[0-9]*$", self.cleaned_data.get('rut')):
            raise forms.ValidationError('Debe ser numerico entre 0-9')

    def clean_dv(self):
        
        Validacion de digito verificador
        
        Metodo que valida que el dv ingresado se encuentre entre los caracteres aceptados 0-9 o K.
        
        Excepciones:
            -ValidationError = Mensaje de error que aparece cuando se ingresan caracteres no coincidentes
        
        if not re.match("^[0-9,'k','K']*$", self.cleaned_data.get('dv')):
            raise forms.ValidationError('Debe ser numerico entre 1-9, o "K" ')"""
            
    def print_user(self):
        return self.cleaned_data.get('username')

    def clean_password(self):
        """
        Validacion de contraseña
        
        Metodo que valida que ambas contraseñas ingresadas sean iguales, esto antes de ser encriptadas
        y almacenadas en la base de datos.
        
        Excepciones:
            -ValidationError = Mensaje de error que aparece cuando las contraseñas no coinciden 
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('¡Contraseñas no coinciden!')
        return password2
    

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
