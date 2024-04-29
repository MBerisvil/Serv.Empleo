from django.contrib import admin
from seapp.models import Persona,EstudioRealizado,ExperienciaLaboral,InformacionAdicional, Contacto

# Register your models here.

class PersonaAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class EstudioRealizadoAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class ExperienciaLaboralAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class InformacionAdicionalAdmin(admin.ModelAdmin):
    readonly_fields=('created','updated')

class AbstractUser(admin.ModelAdmin):
    list_display = ('username', 'email','first_name', 'last_name', 'is_enterprise')





admin.site.register(Persona)
admin.site.register(EstudioRealizado)
admin.site.register(ExperienciaLaboral)
admin.site.register(InformacionAdicional)
admin.site.register(Contacto)

