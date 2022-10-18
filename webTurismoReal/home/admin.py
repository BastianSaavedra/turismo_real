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

class DepartamentoAdmin(admin.ModelAdmin):

    autocomplete_fields = ['comuna']

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
admin.site.register(Reserva)
