from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
# <<<<<<< HEAD
from datetime import datetime
# =======
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# >>>>>>> origin/branch_SebastianZuniga

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, username, 
                    nombre, ap_paterno, ap_materno, 
                    rut, dv, telefono, password=None):
        if not correo:
            raise ValueError('El usuario debe tener un correo electronico')
        
        usuario = self.model(username = username,
                             correo = self.normalize_email(correo),
                             nombre = nombre, 
                             ap_paterno = ap_paterno,
                             ap_materno = ap_materno,
                             rut = rut,
                             dv = dv,
                             telefono = telefono
                             )
        usuario.set_password(password)
        usuario.usuario_cliente = True
        usuario.save()
        return usuario
    
    def create_superuser(self,username, correo, nombre, ap_paterno, ap_materno, rut, dv, telefono, password):
        usuario = self.create_user(
            correo,
            username=username,
            nombre = nombre,
            ap_paterno = ap_paterno,
            ap_materno = ap_materno,
            rut = rut,
            dv = dv,
            telefono = telefono,
            password=password
            )
        usuario.usuario_superAdministrador = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique = True, max_length=40)
    nombre = models.CharField('Nombre', max_length=50)
    ap_paterno = models.CharField('Apellido paterno', max_length=50)
    ap_materno = models.CharField('Apellido materno', max_length=50)
    rut = models.CharField('RUT', max_length=8)
    dv = models.CharField('Dv', max_length=1)
    correo = models.EmailField('Correo electronico', max_length=100, unique=True)
    telefono = models.CharField('Telefono', max_length=12)
    usuario_superAdministrador = models.BooleanField(default=False)
    usuario_admin = models.BooleanField(default=False)
    usuario_cliente = models.BooleanField(default=True)
    usuario_funcionario = models.BooleanField(default=False)
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','ap_paterno','ap_materno',
                       'rut','dv','correo','telefono']
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_superAdministrador
    
    def is_admin(self):
        return self.usuario_admin
    
    def is_cliente(self):
        return self.usuario_cliente
    
    def is_funcionario(self):
        return self.usuario_funcionario

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
    # img = models.ImageField(upload_to="comunas", default="../static/default/default.png", null=True)

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

class ImagenDepartamento(models.Model):
    imagen = models.ImageField(upload_to="departamentos", default="../static/default/default.png" )
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="imagenes")

class DetalleDpto(models.Model):
    # departamento = models.OneToOneField(
    #     Departamento, on_delete=models.CASCADE, null=False, blank=False
    # )
    
    DPTO_STATUS = (
        ("1", "Disponible"),
        ("2", "Mantencion"),
        ("3", "No Disponible")
    )

    OPCIONES = (
      ('se','Seleccione'),
      ('SI','SI'),
      ('NO','NO')
    )

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="detalle")
    precio = models.PositiveBigIntegerField(default=0, blank=False)
    capacidad = models.IntegerField()
    
    amoblado = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cable = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    electronicos = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    internet = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    aire_acondicionado = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    bodega = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    bannio = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_bannio = models.PositiveIntegerField(default=0, blank=True)
    dormitorio = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_dormitorio = models.PositiveIntegerField(default=0, blank=True)
    estacionamiento = models.CharField(max_length=2, choices=OPCIONES, blank=False, default="se")
    cant_estacionamiento = models.PositiveIntegerField(default=0, blank=True)

    status = models.CharField(choices=DPTO_STATUS, max_length=13, default="1")
    inicio_mantencion = models.DateTimeField(default=datetime.now, blank=True)
    fin_mantencion = models.DateTimeField(default=datetime.now, blank=True)
    cant_dias_mantencion = models.IntegerField(default=0)

    def __str__(self):
        return self.departamento.titulo

    class Meta:
        db_table = 'detalle_dpto'
        verbose_name = 'Detalle departamento'
        verbose_name_plural = 'Detalles de Departamentos'
        
class Tour(models.Model):
    
    TOUR_STATUS = (
        ("1", "Disponible"),
        ("2", "No Disponible")
    )
    
    TIPO_TR = (
        ("0", "Seleccione"),
        ("1", "Turismo Cultural"),
        ("2", "Turismo de Naturaleza"),
        ("3", "Turismo Gastronomico")
    )
    
    tipoTour = models.CharField(max_length=100, choices=TIPO_TR, default="0", blank=True, null=True)
    nombreTour = models.CharField(max_length=200, blank=True, null=True)
    horario_in = models.TimeField(default='00:00', blank=True, null=True)
    horario_fin = models.TimeField(default='00:00', blank=True, null=True)
    costo = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    comuna = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(choices=TOUR_STATUS, max_length=13, default="1")
    
    def __str__(self):
        return self.nombreTour

    class Meta:
        db_table = 'tour'
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'
    
class Conductor(models.Model):
    
    CONDUCTOR_STATUS = (
        ('1', 'Activo'),
        ('2', 'Inactivo')
    )

    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    edad = models.PositiveIntegerField(default=0, blank=True, null=True)
    annio_experiencia = models.PositiveIntegerField(default=0, blank=True, null=True)
    status = models.CharField(choices=CONDUCTOR_STATUS, max_length=13, default="1")
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'conductor'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'

class Marca(models.Model):
    marca = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.marca

    class Meta:
        db_table = 'marca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

class Modelo(models.Model):
    modelo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelo")
    
    def __str__(self):
        return self.modelo

    class Meta:
        db_table = 'modelo'
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        
class Transporte(models.Model):


    TRANSPORTE_STATUS = (
        ('1', 'Activo'),
        ('2', 'Inactivo')
    )
    
    TIPOS_TRANSPORTE = (
        ("0", "Seleccione"),
        ("1", "Taxi"),
        ("2", "Furgoneta"),
        ("3", "Bus")
    )
    
    patente = models.CharField(max_length=6, blank=True, null=True)
    tipo_transporte = models.CharField(max_length=30, choices=TIPOS_TRANSPORTE, default="0", blank=True, null=True)
    annio = models.PositiveIntegerField(default=0, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    num_puertas = models.PositiveIntegerField(default=0, blank=True, null=True)
    kmRecorridos = models.PositiveIntegerField(default=0, blank=True, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, related_name="transporte")
    status = models.CharField(choices=TRANSPORTE_STATUS, max_length=12, default="1")
     
    def __str__(self):
        return self.patente

    class Meta:
        db_table = 'transporte'
        verbose_name = 'Transporte'
        verbose_name_plural = 'Trasportes'
    
class DetalleTP(models.Model):
    
    TRASLADO_STATUS = (
        ("1", "Disponible"),
        ("2", "No Disponible")
    )

    lugar_tp = models.CharField(max_length=200, blank=True, null=True)
    horario_in = models.TimeField(default='00:00', blank=True, null=True)
    horario_fin = models.TimeField(default='00:00', blank=True, null=True)
    costo_tp = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)
    status = models.CharField(choices=TRASLADO_STATUS, max_length=12, default="1")
    
    def __str__(self):
        return self.transporte.patente

    class Meta:
        db_table = 'detalleTP'
        verbose_name = 'Detalle Transporte'
        verbose_name_plural = 'Detalle de Transportes'

class Reserva(models.Model):

    RESERVA_STATUS = (
        ('1', 'Activa'),
        ('2', 'Cancelada'),
        ('3', 'Terminada'),
        ('4', 'En Proceso'),
        ('5', 'En Espera')
    )

    ESTADIA = (
        ('0', 'Seleccionar'),
        ('1', 'Arribo'),
        ('2', 'No Arribo'),
    )

    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    date_joined = models.DateField(default=datetime.now)
    detalle_dpto = models.ForeignKey(DetalleDpto, on_delete=models.CASCADE, related_name="detalleDpto")
    guest = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, default="null")
    cant_dias_reserva = models.IntegerField(default=0)
    costo_reserva = models.IntegerField(default=0)
    total_reserva = models.IntegerField(default=0)
    huespedes = models.IntegerField(default=0)


    status = models.CharField(choices=RESERVA_STATUS, max_length=12, default="1")
    status_estadia = models.CharField(choices=ESTADIA, max_length=13, default="0")
    mensaje_check_in = models.TextField(blank=True)
    mensaje_check_out = models.TextField(blank=True)
    costo_multa = models.IntegerField(default=0)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    detalle_tp = models.ForeignKey(DetalleTP, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.guest.username

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'


class BookingOrder(models.Model):
    user = models.ForeignKey(Usuario, models.DO_NOTHING)
    reserva = models.ForeignKey(Reserva, models.DO_NOTHING)
    token_ws = models.CharField(max_length=255, default='0')
    tarjeta = models.CharField(max_length=10, default='0')
    # fecha_transbank = models.CharField(max_length=100, default='0')
    estado_transbank = models.CharField(max_length=100, default='0')
    total = models.PositiveIntegerField(default=0)
    fecha = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"N°{self.id}"

    class Meta:
        db_table = 'orden_de_reserva'
        verbose_name = 'Order de Reserva'
        verbose_name_plural = 'Ordenes de Reservas'



    


