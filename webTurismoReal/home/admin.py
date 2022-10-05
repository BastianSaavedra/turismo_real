from django.contrib import admin
from .models import *


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

admin.site.register(Departamento)
admin.site.register(DetalleDpto)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Reserva)
