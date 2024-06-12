from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core.validators import EmailValidator

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("El nombre de usuario dado no existe")
        
    
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_user(self, username=None, password=None,**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password,**extra_fields)
    
    def create_superuser(self, username=None, password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password,**extra_fields)


class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('asistente', 'Asistente Medico'),
        ('doctor', 'Doctor'),
    )

    username = models.CharField(max_length=36, blank=True,unique=True)
    rol = models.CharField(max_length=15, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_rol(self):
        # Busca el valor del rol en la lista de opciones ROLES
        for rol_value, rol_display in self.ROLES:
            if rol_value == self.rol:
                return rol_display

        # Si no se encuentra el rol, devuelve una cadena vacía
        return ""







class Paciente(models.Model):
    SEXO=(
        ('mujer', 'Mujer'),
        ('hombre', 'Hombre')
    )
    id_paciente = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10, choices=SEXO)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    cid = models.CharField(max_length=15, blank=True)
    notas = models.TextField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=255, validators=[EmailValidator()], blank=True)
    def __str__(self):
        return(f"{self.nombre}")
    def get_full_name(self):
        return(f"{self.nombre} {self.apellido}")
    def get_short_name(self):
        return(f"{self.nombre}")
    
class Doctor(models.Model):

    ESPECIALIDAD = (
        ('odontologia', 'Odontologia'),
        ('nutricionista','Nutricionista'),
        ('general', 'Medicina General'),
        ('pediatria', 'Pediatria'),
        ('orientacion','Orientación Estudiantil y Familiar'),

    )
    SEXO=(
        ('mujer', 'Mujer'),
        ('hombre', 'Hombre')
    )
    id_doctor = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10, choices=SEXO)
    cid = models.CharField(max_length=15, blank=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    especialidad = models.CharField(max_length=15, choices=ESPECIALIDAD)
    user_ref = models.ForeignKey(User, on_delete=models.RESTRICT)
    direccion =  models.TextField(blank=True, null=True)
    notas = models.TextField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=255, validators=[EmailValidator()], blank=True)
    def __str__(self):
        return(f"{self.nombre}")
    def get_full_name(self):
        return(f"{self.nombre} {self.apellido}")
    def get_short_name(self):
        return(f"{self.nombre}")
    
class Asistente(models.Model):
    SEXO=(
        ('mujer', 'Mujer'),
        ('hombre', 'Hombre')
    )
    id_asistente = models.AutoField(primary_key=True)
    creado_en = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10, choices=SEXO)
    cid = models.CharField(max_length=15, blank=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    user_ref = models.ForeignKey(User, on_delete=models.RESTRICT)
    doctor_ref = models.ForeignKey(Doctor, on_delete=models.RESTRICT, null=True)
    notas = models.TextField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=255, validators=[EmailValidator()], blank=True)
    def __str__(self):
        return(f"{self.nombre}")
    def get_full_name(self):
        return(f"{self.nombre} {self.apellido}")
    def get_short_name(self):
        return(f"{self.nombre}")
    
class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=250, blank=True, null=True)
    cant_disponible = models.PositiveIntegerField()
    image_url = models.CharField(max_length=250, null=True, blank=True)
    notas = models.TextField(max_length=250, blank=True, null=True)
    def __str__(self):
        return(f"{self.nombre}")


class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    asistente = models.ForeignKey(Asistente,  on_delete=models.CASCADE, null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete= models.CASCADE)
    titulo = models.CharField(max_length=250)
    diagnostico = models.TextField(max_length=250)
    tratamiento = models.TextField(max_length=250, blank=True)
    fecha_propuesta = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    medicamentos = models.ManyToManyField(Medicamento, through='Recipe')
    def __str__(self):
        return f'Cita de {self.paciente.get_full_name()} con el doctor {self.doctor.get_full_name()}. Fecha: {self.fecha_propuesta.date()}' 
    
    def verificar_cita(self):
        fecha_propuesta_sin_hora = self.fecha_propuesta.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_actual_sin_hora = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Calcula la diferencia entre las fechas (solo en días)
        dias_restantes = (fecha_propuesta_sin_hora - fecha_actual_sin_hora).days
        print(dias_restantes)
        return dias_restantes
        

 #Esto actual como una tabla Muchos a muchos entre Citas y Medicamentos.
class Recipe(models.Model): 
    id_recipe = models.AutoField(primary_key=True)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad_deseada = models.PositiveIntegerField()
    nota = models.TextField(max_length=250, blank=True, null=True)
    def __str__(self):
        return f'{self.medicamento} en cita: {self.cita}; cantidad = {self.cantidad_deseada}'
    


        

    