from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import View,TemplateView, FormView
from .forms import Persona_Form,Empresa_Form, EstudioRealizado_Form, Contacto_Form, CrearUsuarioForm, InformacionAdicional_Form, \
    ExperienciaLaboral_Form, UserRegistrationForm, GroupUserForm
from .models import Persona, EstudioRealizado, InformacionAdicional, ExperienciaLaboral
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Q



# Create your views here.
def base(request):
    return render(request, "seapp/base.html")

#@login_required  # Decorador para que solo los usuarios logueados puedan acceder
def index(request):
    return render(request, "seapp/index.html")

def nosotros(request):
    return render(request, "seapp/nosotros.html")

@login_required
def persona(request):

    data = {
        'form' : Persona_Form(),
        'form2' : Empresa_Form(),

    }

    if request.method == 'POST':
        formulario = Persona_Form(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Datos Cargados.")
            data["message"] = "Datos cargados"
        else:
            data["form"] = formulario

    if request.method == 'POST':
        formulario = Empresa_Form(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Datos Cargados.")
            data["message"] = "Datos cargados"
        else:
            data["form2"] = formulario  

 
    return render(request, "seapp/persona.html", data)

def modificar_persona(request, id):

    persona = get_object_or_404(Persona, id=id)

    data = {
        'form' : Persona_Form(instance=persona)
    }

    if request.method == 'POST':
        formulario = Persona_Form(data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="persona.html")
        data["form"] = formulario

    return render(request, "seapp/modificarpersona.html", data)

# -- REVISAR FORMULARIO --***
@login_required
def estudiorealizado(request):
    data = {

        "form" : EstudioRealizado_Form()
    }
    

    if request.method == 'POST':
        formulario = EstudioRealizado_Form(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Datos Cargados.")
            data["message"] = "Datos Cargados"
        else:
            data["form"] = formulario

    return render(request, "seapp/estudiorealizado.html",data)

def contacto(request):

    
    if request.method == 'POST':
        form = Contacto_Form(data=request.POST)
        if form.is_valid():
            send_mail(
                'Serv.Empleo:' + form.cleaned_data['asunto'],
                form.cleaned_data['mensaje'], 
                form.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
        )
        form.save()
        messages.success(request, "Mensaje enviado.")

    return render(request, "seapp/contacto.html")

   
    """
    data = {
        'form' : Contacto_Form()
    }

    if request.method == 'POST':
        formulario = Contacto_Form(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Consulta enviada.")
            data["message"] = "Consulta Enviada"
        else:
            data["form"] = formulario
    return render(request, "seapp/contacto.html", data)
    

    -----ASI ENVIA EMAIL----
    def contacto(request):
    
    data = {
        'form' : Contacto_Form()
    }

    if request.method == 'POST':
        formulario = Contacto_Form(data=request.POST)
        if formulario.is_valid():
            send_mail(
                formulario.cleaned_data['asunto'],
                formulario.cleaned_data['mensaje'], 
                formulario.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
        )
            messages.success(request, "Mensaje enviada.")

    return render(request, "seapp/contacto.html",data)
    

    """

@login_required
def listado_candidatos(request):
    busqueda = request.POST.get("buscar")
    persona = Persona.objects.all()
    estudiorealizado = EstudioRealizado.objects.all()

    # Creando un paginador
    paginador = Paginator(persona, 10)
    page = request.GET.get('page')
    page_obj = paginador.get_page(page)

    if busqueda:
        persona = Persona.objects.filter(
            Q(nombre__icontains=busqueda)|
            Q(apellido__icontains=busqueda)|
            Q(email__icontains=busqueda)
        ).distinct()
        if busqueda:
            estudiorealizado = EstudioRealizado.objects.filter(
                Q(carrera__icontains=busqueda)
            ).distinct() 
        else:
            messages.error(request, "Candidato no encontrado")
    else:
        messages.error(request, "Candidato no encontrado")

    data = {
        'persona' : persona,
        'estudiorealizado' : estudiorealizado,
        'page_obj' : page_obj

    }

    return render(request, "seapp/listadocandidatos.html",data)

def registrarse(request):

    data = {
        'form' : CrearUsuarioForm()
    }
    if request.method == 'POST':
        formulario = CrearUsuarioForm(data=request.POST)
        formulario = Persona_Form(data=request.POST)
        if formulario.is_valid():

            #Send Email Welcome
            send_mail(
                'Bienvenido a Serv.Empleo',
                'Gracias por registrarte en nuestra plataforma. Esperamos que encuentres un buen puesto de trabajo o candidato.',
                formulario.cleaned_data["username"],
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            if user.is_enterprise:
                group = Group.objects.get(name='Empresas')
                user.groups.add(group)  
                messages.success(request, "Te has registrado correctamente")
                return redirect(to="index.html")
            else:
                group = Group.objects.get(name='Candidatos')
                user.groups.add(group)
                messages.success(request, "Te has registrado correctamente")
            #redirigir al Home
            return redirect(to="index.html")
        data ["form"] = formulario

    return render(request, "registration/registrarseCan.html", data)

# Eliminar, desactivar usuario desde Dashboard
@user_passes_test(lambda u: u.groups.filter(name='Administrador').exists())
def desactivar_usuario(request, pk):

    usuario = get_object_or_404(User, id=pk)
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, "Usuario desactivado correctamente")
    else:
        usuario.is_active = True
        usuario.save()
        messages.success(request, "Usuario activado correctamente")


    return redirect(to="dashboard.html")

@user_passes_test(lambda u: u.groups.filter(name='Administrador').exists())
def eliminar_usuario(request, pk):

    usuario = get_object_or_404(User, id=pk)
    if usuario:
        usuario.delete()
        
        messages.success(request, "Usuario eliminado correctamente")


    return redirect(to="dashboard.html")

@login_required
def informacionadicional(request):
    
    data = {

        'form' : InformacionAdicional_Form()
    }

    if request.method == 'POST':
        formulario = InformacionAdicional_Form(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Información Adicional Registrada Correctamente!")
            data['message']="Información Adicional Registrada!"
        else:
            data["form"] = formulario

    return render(request, "seapp/informacionadicional.html", data)

@login_required
def experiencialaboral(request):
    data = {
        'form' : ExperienciaLaboral_Form(),
    }
    
    if request.method == 'POST':
        formulario = ExperienciaLaboral_Form(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Experiencia Laboral Registrada!")
            data ['message']= "Experiencia laboral registrada"
        else:
            data["form"] = formulario

    return render(request, "seapp/experiencialaboral.html", data)

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

# Dashboard de Informacion Perfil Administrados.
def dashboard(request):
    busqueda = request.POST.get("buscar")
    usuarios = User.objects.all()


    if busqueda:
        usuarios = User.objects.filter(
            Q(username__icontains=busqueda)|
            Q(first_name__icontains=busqueda)|
            Q(last_name__icontains=busqueda)
        ).distinct()
    else:
        messages.error(request, "No se encontraron resultados para la busqueda")
              
    data ={
            'User' : usuarios,
        }
    
    return render(request, 'seapp/dashboard.html', data)

def ver_candidato(request, pk):

    candidato = get_object_or_404(Persona, id=pk)
    estudiorealizado = get_object_or_404(EstudioRealizado, persona_estu_realizado=candidato)


    if estudiorealizado.persona_estu_realizado == None:
        messages.info(request, "Este candidato no tiene estudios registrados.")
        if estudiorealizado.persona_estu_realizado >= 1:
            messages.info(request, f"Este candidato tiene {estudiorealizado.persona_estu_realizado} estudio registrado.")
    

    data = {
        'Candidato' : candidato,
        'Estudiorealizado' : estudiorealizado,

    }


    return render(request, 'seapp/ver_candidato.html',data)


#enviar email de bienvenida a los usuarios
#CODIGO EN DESUSO
"""def email_bienvenida_email(user):

    email = EmailMessage(
        subject='Bienvenido a Sistema de Empleo',
        body='Hola'+ user.username + 
        if user.is_enterprise():
                ', bienvenido al sistema de empresas, aquí las empresas podrán publicar sus vacantes y buscar candidatos.'
        else:
        ', bienvenido al sistema de empleo, aquí podrás aplicar a empleo y buscar empleos.'
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    email.send()"""
"""def registrarseOpc(request):

    return render(request, "registration/registrarseOpc.html")

def registrarseCan(request):

    return render(request, "registration/registrarseCan.html")

def registrarseEmp(request):

    return render(request, "registration/registrarseEmp.html")"""
