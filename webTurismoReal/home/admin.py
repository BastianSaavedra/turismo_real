from django.contrib import admin
from .models import *

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nombre', 'ap_paterno')
    ordering = ('id', 'username','nombre')
    search_fields = ('id','username')
    list_display_links = ('username',)


class RegionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'nombre'),
    ordering = ['nombre']

class ComunaAdmin(admin.ModelAdmin):
    search_fields = ('id', 'nombre')
    autocomplete_fields = ['region']

class ImagenDepartamentoAdmin(admin.TabularInline):
    model = ImagenDepartamento

class DepartamentoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['comuna']
    inlines = [
        ImagenDepartamentoAdmin
    ]
    
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido','edad','annio_experiencia')
    ordering = ('id', 'nombre')
    search_fields = ('id','nombre')

class ModeloAdmin(admin.ModelAdmin):
    list_display = ('id', 'modelo', 'marca')
    ordering = ('id', 'marca')
    search_fields = ('id','modelo', 'marca')
    
class TransporteAdmin(admin.ModelAdmin):
    list_display = ('id', 'patente', 'tipo_transporte', 'modelo','conductor')
    ordering = ('id', 'tipo_transporte')
    search_fields = ('id','patente', 'tipo_transporte', 'conductor')
    
class DetalleTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'lugar_tp', 'costo_tp', 'transporte')
    ordering = ('id', 'lugar_tp')
    search_fields = ('id','lugar_tp', 'transporte')
 
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreTour', 'tipoTour', 'comuna')
    ordering = ('id', 'nombreTour')
    search_fields = ('id','nombreTour', 'tipoTour', 'comuna')   
    
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'booking_id','check_in','check_out','status','tour','detalle_tp')
    ordering = ('id', 'guest')
    search_fields = ('id','guest','booking_id','status')


# class DepartamentoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'direccion', 'precio')
#     search_fields = ('id', 'direccion', 'precio')
#
# class ComunaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nombre')
#     search_fields = ('id', 'nombre')
#
#
# class RegionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nombre')
#     search_fields = ('id', 'nombre')
#
# class ReservaAdmin(admin.ModelAdmin):
#     list_display = ('user', 'cant_acompaniantes', 'fecha_inicio',
#         'fecha_termino', 'total_pago'
#     )
#     search_fields = ('user', 'cant_acompaniantes', 'fecha_inicio',
#         'fecha_termino', 'total_pago')

# admin.site.register(Departamento, DepartamentoAdmin)
# admin.site.register(DetalleDpto)
# admin.site.register(Comuna, ComunaAdmin)
# admin.site.register(Region, RegionAdmin)
# admin.site.register(Reserva, ReservaAdmin)

# <<<<<<< HEAD
admin.site.register(Departamento, DepartamentoAdmin)
# =======
admin.site.register(Usuario, UsuariosAdmin)
# >>>>>>> origin/branch_SebastianZuniga
admin.site.register(DetalleDpto)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Marca)
admin.site.register(Modelo, ModeloAdmin)
admin.site.register(Conductor, ConductorAdmin)
admin.site.register(Transporte, TransporteAdmin)
admin.site.register(DetalleTP, DetalleTPAdmin)
admin.site.register(Tour, TourAdmin)
