from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from datetime import date

def validar_fecha(value):

    if value > date.today():

        raise ValidationError(
            "La fecha no puede ser posterior al día actual"
        )


class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    domicilio = models.TextField()
    foto = models.ImageField(
        upload_to='usuarios/',
        blank=True,
        null=True
    )


    modelo_dron = models.CharField(max_length=100)
    num_serie_dron = models.CharField(max_length=100)
    fecha_act_dron = models.DateField(
        validators=[validar_fecha]
    )


    num_serie_generador = models.CharField(max_length=100)
    modelo_generador = models.CharField(max_length=100)
    fecha_act_generador = models.DateField(
        validators=[validar_fecha]
    )


    num_serie_control = models.CharField(max_length=100)
    fecha_act_control = models.DateField(
        validators=[validar_fecha]
    )


    def save(self,*args,**kwargs):

        if not self.contrasena.startswith(
            'pbkdf2_sha256$'
        ):

            self.contrasena = make_password(
                self.contrasena
            )


        super().save(*args,**kwargs)


class Administrador(models.Model):

    nombre_admin = models.CharField(max_length=200)

    correo_admin = models.EmailField(unique=True)

    contrasena_admin = models.CharField(max_length=255)

    telefono_admin = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    foto_admin = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.contrasena_admin.startswith('pbkdf2_sha256$'):
            self.contrasena_admin = make_password(
                self.contrasena_admin
            )

        super().save(*args, **kwargs)


def save(self, *args, **kwargs):
    if not self.contrasena_admin.startswith('pbkdf2_sha256$'):
        self.contrasena_admin = make_password(self.contrasena_admin)
    super().save(*args, **kwargs)

# ------------------------ CITA ---------------------------------------------

class Cita(models.Model):

    ESTATUS_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("En proceso", "En proceso"),
        ("Completado", "Completado"),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )

    nombre_completo = models.CharField(max_length=200)
    modelo_dron = models.CharField(max_length=100)
    equipo = models.CharField(max_length=100)
    tipo_servicio = models.CharField(max_length=50)
    fecha_cita = models.DateField()
    hora_cita = models.CharField(max_length=10)
    descripcion = models.TextField()

    estatus = models.CharField(
        max_length=20,
        choices=ESTATUS_CHOICES,
        default='Pendiente'
    )

    def __str__(self):
        return self.nombre_completo
    
# ------------------ RECUPERAR CONTRASEÑA -------------------
class RecuperarPassword(models.Model):

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    fecha_creacion = models.DateTimeField(
        default=timezone.now
    )


    def __str__(self):
        return self.usuario.correo