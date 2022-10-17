from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Region(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'


class Comuna(models.Model):
    nombre = models.CharField(max_length=150)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    img = models.ImageField(upload_to="comunas", default="../static/default/default.png")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'comuna'
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'


class Departamento(models.Model):

    titulo = models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=150)
    comuna = models.ForeignKey(Comuna, models.DO_NOTHING)
    descripcion = models.TextField()


    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class DetalleDpto(models.Model):
    # departamento = models.OneToOneField(
    #     Departamento, on_delete=models.CASCADE, null=False, blank=False
    # )
    
    DPTO_STATUS = (
        ("1", "disponible"),
        ("2", "no disponible")
    )

    OPCIONES = (
      ('se','Seleccione'),
      ('SI','SI'),
      ('NO','NO')
    )

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    precio = models.PositiveBigIntegerField(default=0)
    capacidad = models.IntegerField()
    
    amoblado = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cable = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    electronicos = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    internet = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    aire_acondicionado = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    bodega = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    bannio = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_bannio = models.PositiveIntegerField(default=0)
    dormitorio = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_dormitorio = models.PositiveIntegerField(default=0)
    estacionamiento = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_estacionamiento = models.PositiveIntegerField(default=0)

    status = models.CharField(choices=DPTO_STATUS, max_length=13)

    def __str__(self):
        return self.departamento.titulo

    class Meta:
        db_table = 'detalle_dpto'
        verbose_name = 'Detalle departamento'
        verbose_name_plural = 'Detalles de Departamentos'


class Reserva(models.Model):

    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    date_joined = models.DateField(default=datetime.now)
    detalle_dpto = models.ForeignKey(DetalleDpto, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, default="null")
    cant_dias_reserva = models.IntegerField(default=0)
    total_reserva = models.IntegerField(default=0)

    def __str__(self):
        return self.guest.username

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

class UsersMetadata(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    rut = models.PositiveIntegerField()
    dv = models.CharField(max_length=1)








