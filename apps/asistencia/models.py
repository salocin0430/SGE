from django.db import models

# Create your models here.

class Asistencia(models.Model):
	fecha_registro = models.DateTimeField(auto_now=True)
	asistencia_hombres = models.IntegerField()
	asistencia_mujeres = models.IntegerField()
	asistencia_jovenes = models.IntegerField()
	asistencia_adolecentes = models.IntegerField()
	asistencia_niños = models.IntegerField()
	dia = models.CharField(max_length=50)