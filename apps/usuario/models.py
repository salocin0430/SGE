from django.db import models
from PIL import Image
# Create your models here.

class Usuario(models.Model):
	fecha_registro = models.DateTimeField(auto_now=True)
	nombres = models.CharField(max_length=50) #
	apellidos = models.CharField(max_length=50) #
	fecha_nacimiento = models.DateField() #
	lugar_nacimiento = models.CharField(max_length=50) #
	edad = models.IntegerField() #
	estado_civil = models.CharField(max_length=50) #
	profesion = models.CharField(max_length=50) #
	telefono = models.CharField(max_length=50,null=True, blank=True) #
	direccion = models.CharField(max_length=50) #
	barrio = models.CharField(max_length=50) #
	fecha_conversion = models.DateField() #
	lugar_conversion = models.CharField(max_length=50) #
	iglesia_conversion = models.CharField(max_length=50) #
	pastor_conversion = models.CharField(max_length=50) #
	fecha_bautismo = models.DateField() #
	lugar_bautismo = models.CharField(max_length=50) #
	iglesia_bautismo = models.CharField(max_length=50) #
	pastor_bautismo = models.CharField(max_length=50) #
	observaciones = models.TextField(null=True, blank=True)
	image = models.FileField(null=True, blank=True) #

	def __str__(self):
		return '{} {}'.format(self.nombres, self.apellidos)

class Conyuge_hijos(models.Model):
	tipo = models.CharField(max_length=50)
	nombres_familiar = models.CharField(max_length=50)
	apellidos_familiar = models.CharField(max_length=50)
	edad_familiar = models.IntegerField()
	usuario  = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	