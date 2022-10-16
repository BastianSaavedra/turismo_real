from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
                             telefono = telefono)

        usuario.set_password(password)
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
        usuario.usuario_administrador = True
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
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','ap_paterno','ap_materno',
                       'rut','dv','correo','telefono']
    
    def __str__(self):
        return f'{self.nombre},{self.ap_paterno}'
    
    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador



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
        return f"{self.titulo}-{self.comuna}"

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
    detalle_dpto = models.ForeignKey(DetalleDpto, on_delete=models.CASCADE)
    guest = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, default="null")

    def __str__(self):
        return self.guest.username

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

# class UsersMetadata(models.Model):
#     user = models.ForeignKey(User, models.DO_NOTHING)
#     rut = models.PositiveIntegerField()
#     dv = models.CharField(max_length=1)


