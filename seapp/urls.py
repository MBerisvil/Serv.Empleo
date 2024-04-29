from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


admin.site.site_header = "Servicio de Empleo"
admin.site.site_title = "Servicio de Empleo"
admin.site.index_title = "Servicio de Empleo"

urlpatterns = [
    path('', views.index, name='index.html'),
    path('nosotros/', views.nosotros, name='nosotros.html'),
    path('base/', views.base, name='base.html'),
    path('persona/', views.persona, name='persona.html'),
    path('estudiorealizado/', views.estudiorealizado, name='estudiorealizado.html'),
    path('contacto/', views.contacto, name='contacto.html'),
    path('listadocandidatos/', views.listado_candidatos, name='listadocandidatos.html'),
    path('modificarpersona/<int:pk>/', views.modificar_persona, name='modificarpersona.html'),
    path('registrarse/', views.registrarse, name='registrarse.html'),
    #path('registrarseOpc/', views.registrarseOpc, name='registrarseOpc.html'),
    #path('registrarseCan/', views.registrarseCan, name='registrarseCan.html'),
    #path('registrarseEmp/', views.registrarseEmp, name='registrarseEmp.html'),
    path('informacionadicional/', views.informacionadicional, name='informacionadicional.html'),
    path('experiencialaboral/', views.experiencialaboral, name='experiencialaboral.html'),
    path('dashboard/', views.dashboard, name='dashboard.html'),
    path('desactivar_usuario/<int:pk>/', views.desactivar_usuario, name='desactivar_usuario.html'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario.html'),
    path('ver_candidato/<int:pk>/', views.ver_candidato, name='ver_candidato.html'),

]