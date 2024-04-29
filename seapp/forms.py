from django import forms    
from .models import Persona, EstudioRealizado, Contacto, InformacionAdicional, ExperienciaLaboral
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group



class Persona_Form(forms.ModelForm):
    
    class Meta:
        model = Persona
        #fields = '__all__'
        fields = ["nombre","apellido","dni","email","telefono","direccion","fecha_nacimiento",
                  "sexo","localidad","provincia","pais", "image"]
        #fields = ["dni","cuit","nombre","apellido","email","telefono","direccion","fecha_nacimiento","sexo","localidad","provincia","pais", "image"]

class Empresa_Form(forms.ModelForm):

    class Meta:
        model = Persona
        #fields = '__all__'
        fields = ["nombre","cuit","email","telefono","direccion","localidad","provincia","pais", "image"]
        #fields = ["dni","cuit","nombre","apellido","email","telefono","direccion","fecha_nacimiento","sexo","localidad","provincia","pais"]

class EstudioRealizado_Form(forms.ModelForm):

    class Meta:
        model= EstudioRealizado
        fields = '__all__'
        #fields = ["carrera","niv_academico","esta_estudios","persona_estu_realizado"]

class Contacto_Form(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ["nombre","email","mensaje","asunto"]

class CrearUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "is_enterprise", "last_name", "password1", "password2",] 

class InformacionAdicional_Form(forms.ModelForm):

    class Meta:
        model = InformacionAdicional
        fields = '__all__'

class ExperienciaLaboral_Form(forms.ModelForm):

    class Meta:
        model = ExperienciaLaboral
        fields = '__all__'

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_enterprise']

class GroupUserForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


