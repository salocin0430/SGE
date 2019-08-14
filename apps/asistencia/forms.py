# -*- encoding:utf-8 -*-
from django import forms

from apps.asistencia.models import Asistencia

class AsistenciaForm(forms.ModelForm):
	class Meta:
		model = Asistencia

		fields = [
			'asistencia_hombres',
			'asistencia_mujeres',
			'asistencia_jovenes',
			'asistencia_adolecentes',
			'asistencia_niños',
			'dia',
		]
		labels = {
			'asistencia_hombres': 'Cantidad de Hombres Adultos',
			'asistencia_mujeres': 'Cantidad de Mujeres Adultas',
			'asistencia_jovenes': 'Cantidad de Jóvenes',
			'asistencia_adolecentes': 'Cantidad de Adolescentes',
			'asistencia_niños': 'Cantidad de niños',
			'dia' : 'Día'
		}
		widgets = {
			'asistencia_hombres': forms.TextInput(attrs={'class':'form-control'}),
			'asistencia_mujeres': forms.TextInput(attrs={'class':'form-control'}),
			'asistencia_jovenes': forms.TextInput(attrs={'class':'form-control'}),
			'asistencia_adolecentes': forms.TextInput(attrs={'class':'form-control'}),
			'asistencia_niños': forms.TextInput(attrs={'class':'form-control'}),
			'dia': forms.TextInput(attrs={'class':'form-control'}),
		}