from datetime import MINYEAR
from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User
import re

class Registro(forms.Form):
    passwrd = forms.CharField(label='Contraseña',required=True, widget=forms.PasswordInput(
        {'class':'form-control',
         'placeholder':'Contraseña'
        })) 
    passwrd2 = forms.CharField(label='Confirmar contraseña',required=True, widget=forms.PasswordInput(
        {'class':'form-control',
         'placeholder':'Confirmar contraseña'
        }))

""" nombre = forms.CharField(label='Nombre', required=True, min_length=4, max_length=40, widget=forms.TextInput(attrs=
        {'class':'form-control',
         'placeholder':'Nombre',
        }))
    ap_paterno = forms.CharField(label='Apellido paterno', required=True, min_length=4, max_length=40, widget=forms.TextInput(attrs=
        {'class':'form-control',
         'placeholder':'Apellido paterno',
        }))
    ap_materno = forms.CharField(label='Apellido materno', required=True, min_length=4, max_length=40, widget=forms.TextInput(attrs=
        {'class':'form-control',
         'placeholder':'Apellido materno',
        }))
    rut = forms.CharField(label='RUT', required=True, min_length=7, max_length=8, widget=forms.TextInput(attrs=
        {'class':'form-control',
         'placeholder':'Rut',
        }))
    dv_rut = forms.CharField(label='Dv', required=True, max_length=1 , widget=forms.TextInput(attrs=
        {'class':'form-control' }))
    correo = forms.EmailField(label='Correo electronico', required=True, widget=forms.EmailInput(attrs=
        {'class':'form-control',
         'placeholder':'ejemplo@gmail.com'}))
    username = forms.CharField(label='Nombre de usuario', required=True, min_length=5, max_length=40, widget=forms.TextInput(attrs=
        {'class':'form-control',
         'placeholder':'Nombre de usuario',
        }))
    telefono = forms.IntegerField(label='Telefono',required=True, widget=forms.TextInput(
        {'class':'form-control',
         'placeholder':'Digite su numero telefonico'
        }))


    
    def clean_username(self): 
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError('Usuario ya existente')
        return username

    def clean_email(self): 
        correo = self.cleaned_data.get('email')
        if User.objects.filter(email = correo).exists():
            raise forms.ValidationError('Correo ya vinculado')
        return correo
    
    def clean_rut(self):
        if not re.match("^[0-9]*$", self.cleaned_data.get('rut')):
            raise forms.ValidationError('Debe ser numerico entre 0-9')

    def clean_dv(self):
        if not re.match("^[0-9,'k','K']*$", self.cleaned_data.get('dv')):
            raise forms.ValidationError('Debe ser numerico entre 1-9, o "K" ')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('passwrd2')!= cleaned_data.get('passwrd'):
            self.add_error('passwrd2','Las contraseñas no coinciden') 

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            nombre = self.cleaned_data.get('nombre'),
            ap_paterno = self.cleaned_data.get('ap_paterno'),
            ap_materno = self.cleaned_data.get('ap_materno'),
            rut = self.cleaned_data.get('rut'),
            dv = self.cleaned_data.get('dv_rut'),
            correo = self.cleaned_data.get('correo'),
            passwrd = self.cleaned_data.get('passwrd'),
            telefono = self.cleaned_data.get('telefono')
        )
"""