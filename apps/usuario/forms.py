# -*- encoding:utf-8 -*-
from django import forms

from apps.usuario.models import Usuario, Conyuge_hijos

class UsuarioForm(forms.ModelForm):

	class Meta:
		model = Usuario

		fields = [
			'nombres',
			'apellidos',
			'fecha_nacimiento',
			'lugar_nacimiento',
			'edad',
			'estado_civil',
			'profesion',
			'telefono',
			'direccion',
			'barrio',
			'fecha_conversion',
			'lugar_conversion',
			'iglesia_conversion',
			'pastor_conversion',
			'fecha_bautismo',
			'lugar_bautismo',
			'iglesia_bautismo',
			'pastor_bautismo',
			'observaciones',
			'image',
		]
		labels = {
			'nombres': 'Nombres ',
			'apellidos': 'Apellidos ',
			'fecha_nacimiento': 'Fecha de nacimiento ',
			'lugar_nacimiento': 'Lugar de nacimiento ',
			'edad': 'Edad ',
			'estado_civil': 'Estado civil ',
			'profesion': 'Profesión ',
			'telefono': 'Teléfono ',
			'direccion': 'Dirección ',
			'barrio': 'Barrio ',
			'fecha_conversion': 'Fecha de conversión ',
			'lugar_conversion': 'Lugar de conversión ',
			'iglesia_conversion': 'Iglesia de conversión ',
			'pastor_conversion': 'Pastor de conversión ',
			'fecha_bautismo': 'Fecha de bautismo ',
			'lugar_bautismo': 'Lugar de bautismo ',
			'iglesia_bautismo': 'Iglesia de bautismo ',
			'pastor_bautismo': 'Pastor de bautismo ',
			'observaciones': 'Observaciones ',
			'image':'Foto ',
		}
		widgets = {
			'nombres': forms.TextInput(attrs={'class':'form-control'}),
			'apellidos': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_nacimiento': forms.TextInput(attrs={'class':'form-control'}),
			'lugar_nacimiento': forms.TextInput(attrs={'class':'form-control'}),
			'edad': forms.TextInput(attrs={'class':'form-control'}),
			'estado_civil': forms.TextInput(attrs={'class':'form-control'}),
			'profesion': forms.TextInput(attrs={'class':'form-control'}),
			'telefono': forms.TextInput(attrs={'class':'form-control'}),
			'direccion': forms.TextInput(attrs={'class':'form-control'}),
			'barrio': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_conversion': forms.TextInput(attrs={'class':'form-control'}),
			'lugar_conversion': forms.TextInput(attrs={'class':'form-control'}),
			'iglesia_conversion': forms.TextInput(attrs={'class':'form-control'}),
			'pastor_conversion': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_bautismo': forms.TextInput(attrs={'class':'form-control'}),
			'lugar_bautismo': forms.TextInput(attrs={'class':'form-control'}),
			'iglesia_bautismo': forms.TextInput(attrs={'class':'form-control'}),
			'pastor_bautismo': forms.TextInput(attrs={'class':'form-control'}),
			'observaciones': forms.Textarea(attrs={'class':'form-control'}),
			#'image': forms.FileInput(attrs={'class':'form-control', 'name': 'image' }),
		}

class Conyuge_hijosForm(forms.ModelForm):

	class Meta:
		model = Conyuge_hijos
		fields = [
			'tipo',
			'nombres_familiar',
			'apellidos_familiar',
			'edad_familiar',
			'usuario',
		]
		labels = {
			'tipo' : 'Parentesco',
			'nombres_familiar': 'Nombres',
			'apellidos_familiar': 'Apellidos',
			'edad_familiar': 'Edad',
			'usuario': 'Pariente',
		}
		widgets = {
			'tipo': forms.TextInput(attrs={'class':'form-control'}),
			'nombres_familiar': forms.TextInput(attrs={'class':'form-control'}),
			'apellidos_familiar': forms.TextInput(attrs={'class':'form-control'}),
			'edad_familiar': forms.TextInput(attrs={'class':'form-control'}),
			'usuario': forms.Select(attrs={'class': 'form-control'}),
		}