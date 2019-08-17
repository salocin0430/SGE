from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import unicodedata
import six
import re
from apps.usuario.config import pagination

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import cm
from reportlab.lib import colors
# Create your views here.

from django.core.exceptions import PermissionDenied
from mixin import Mixin, mixin
from django.views.generic import TemplateView

from braces import views

import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.pagesizes import A4

from apps.usuario.models import Usuario, Conyuge_hijos
from apps.usuario.forms import UsuarioForm, Conyuge_hijosForm
import math

def pantallaInicio(request):
	return render(request, 'inicio/index.html')	

def mision(request):
	return render(request, 'inicio/mision.html')		

def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def info_usuario(self,pk):
	if self.user.is_superuser:
		# Obtenemos un queryset, para un determinado usuario usando pk.
		try:
			miembros = Usuario.objects.get(id=pk)
			familia = Conyuge_hijos.objects.filter(usuario=miembros)

		except ValueError:
			raise Http404()
		# Creamos un objeto HttpResponse con las cabeceras del PDF correctas.
		response = HttpResponse(content_type='application/pdf')
		# Nos aseguramos que el navegador lo abra directamente.
		#response['Content-Disposition'] = 'attachment; filename="Membresía.pdf"'
		buffer = BytesIO()
		Story=[]
		# Creamos el objeto PDF, usando el objeto BytesIO como si fuera un "archivo".
		p = canvas.Canvas(buffer)

		# Dibujamos cosas en el PDF. Aqui se genera el PDF.
		# Consulta la documentación de ReportLab para una lista completa de funcionalidades.

		p.setFont("Times-Bold", 19)
		p.drawString(140, 760, u"INFORMACIÓN DE MEMBRESIA")
		y_nombre = 715
		cadena=str(miembros.nombres)+ " "+ str(miembros.apellidos)
		y_ocupacion = 0
		if len(cadena)>32:
			c=0
			cadena2=""
			y_ocupacion = 681
			while c<32 or caracter!=" ":
				cadena2=cadena2+cadena[c]
				caracter=cadena[c]
				c+=1
			p.setFont("Helvetica", 16)
			p.drawString(220, y_nombre, cadena2)
			y_nombre-=18
			cadena3=""
			while c<len(cadena):
				cadena3=cadena3+cadena[c]
				c+=1
			p.drawString(220, y_nombre, cadena3)

		if len(cadena)<32:
			p.setFont("Helvetica", 16)
			p.drawString(220, 715, "" + str(miembros.nombres)+ " "+ str(miembros.apellidos))
			y_ocupacion = 694



		#p.setFont("Helvetica", 17)
		#p.drawString(220, 715, "" + str(miembros.nombres)+ " "+ str(miembros.apellidos))


		p.setFont("Helvetica-BoldOblique", 13)
		p.drawString(220, y_ocupacion, "" + str(miembros.profesion))
		p.setFont("Times-Roman", 13)
		p.drawString(240, 666, "Direccion: " + str(miembros.direccion) + " "+ str(miembros.barrio))
		p.drawString(240, 644, "Estado civil: " + str(miembros.estado_civil))
		p.drawString(240, 622, "Edad: " + str(miembros.edad))

		cadena = str(miembros.fecha_registro)
		c=0
		cadena2=""
		while c<10:
			cadena2=cadena2+cadena[c]
			c+=1
		p.setFont("Times-Roman", 13)
		p.drawString(240, 600, "Registrado(a) el: " + cadena2)
		
		#p.drawString(240, 600, "Registrado(a) el: " + str(miembros.fecha_registro))
		
		p.setFont("Helvetica-BoldOblique", 14)
		p.drawString(85, 550, "Información")
		p.drawString(95, 530, "Personal:")
		p.setFont("Times-Roman", 13)
		p.drawString(220, 550, "- Fecha de Nacimiento: " + str(miembros.fecha_nacimiento))
		p.drawString(220, 530, "- Lugar de Nacimiento: " + str(miembros.lugar_nacimiento))
		p.setFont("Helvetica-BoldOblique", 14)
		p.drawString(85, 460, "Información de")
		p.drawString(95, 440, "Conversión:")
		p.setFont("Times-Roman", 13)
		p.drawString(220, 460, "- Fecha de conversión: " + str(miembros.fecha_conversion))
		p.drawString(220, 440, "- Lugar de conversión: " + str(miembros.lugar_conversion))
		p.drawString(220, 420, "- Iglesia de conversión: " + str(miembros.iglesia_conversion))
		p.drawString(220, 400, "- Pastor de conversión: " + str(miembros.pastor_conversion))
		p.setFont("Helvetica-BoldOblique", 14)
		p.drawString(85, 360, "Información de")
		p.drawString(100, 340, "Bautismo:")
		p.setFont("Times-Roman", 13)
		p.drawString(220, 360, "- Fecha de conversión: " + str(miembros.fecha_conversion))
		p.drawString(220, 340, "- Lugar de conversión: " + str(miembros.lugar_conversion))
		p.drawString(220, 320, "- Iglesia de conversión: " + str(miembros.iglesia_conversion))
		p.drawString(220, 300, "- Pastor de conversión: " + str(miembros.pastor_conversion))
		p.setFont("Helvetica-BoldOblique", 14)
		p.drawString(85, 240, "Observaciones:")
		p.setFont("Times-Roman", 13)

		#p.drawImage('static/imagenes/logo_pdf.png' , 510, 755, width=75, height=75)
		#p.drawImage(miembros.image.url , 510, 785, width=50, height=50)
		if miembros.image:
			foto=Image(settings.MEDIA_ROOT + str(miembros.image), width=125, height=125)
			Story.append(foto)
			foto.drawOn(p, 70, 600)
		else:
			p.drawImage('static/imagenes/logo_pdf.png', 70, 600, width=125, height=125)

		styles = getSampleStyleSheet()
		doc = SimpleDocTemplate("my_doc.pdf", pagesize=letter)
		# here you add your rows and columns, these can be platypus objects

		cadena_observaciones = str(miembros.observaciones)
		y_observacion = 235
		if len(cadena_observaciones)<76:
			y_observacion -= 13

		if len(cadena_observaciones)>75 and len(cadena_observaciones)<151:
			y_observacion -=13

		if len(cadena_observaciones)>150 and len(cadena_observaciones)<226:
			y_observacion -=35

		if len(cadena_observaciones)>225 and len(cadena_observaciones)<301:
			y_observacion -=49

		if len(cadena_observaciones)>300 and len(cadena_observaciones)<376:
			y_observacion -=52

		if len(cadena_observaciones)>375 and len(cadena_observaciones)<451:
			y_observacion -=65

		if len(cadena_observaciones)>450 and len(cadena_observaciones)<526:
			y_observacion -=74

		if len(cadena_observaciones)>525 and len(cadena_observaciones)<601:
			y_observacion -=82

		if len(cadena_observaciones)>600 and len(cadena_observaciones)<676:
			y_observacion -=95

		if len(cadena_observaciones)>675 and len(cadena_observaciones)<751:
			y_observacion -=107

		estilo=getSampleStyleSheet()
		estilo.add(ParagraphStyle(name = "Titulo",  alignment=TA_JUSTIFY, fontSize=13, fontName="Times-Roman"))
		titulo = Paragraph(" " + str(miembros.observaciones), estilo['Titulo'])
		Story.append(titulo)
		doc.build(Story)
		titulo.drawOn(p, 85, y_observacion)

		#p.drawString(85,120,'' + str(miembros.observaciones))

		p.setFont("Times-Italic", 9)
		p.drawString(265,40, "ADVERTENCIA")
		p.drawString(78,30, "El uso de la información almacenada en esta base de datos está limitado a fines eclesiásticos de los miembros del Centro")
		p.drawString(217,20, "Evangelístico Pereira, quedando excluido cualquier otro uso.")

		s = ParagraphStyle('parrafos', fontSize = 8, fontName="Times-Roman")
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Parentesco','Nombre','Apellido','Edad')
		#Creamos una lista de tuplas que van a contener a las personas
		detalles = [(parientes.tipo, parientes.nombres_familiar, parientes.apellidos_familiar, parientes.edad_familiar) for parientes in familia]
		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[3.5 * cm, 5 * cm, 5 * cm, 2 * cm])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
		[
			#La primera fila(encabezados) va a estar centrada
			('ALIGN',(0,0),(3,0),'CENTER'),
			#Los bordes de todas las celdas serán de color negro y con un grosor de 1
			('GRID', (0, 0), (-1, -1), 1, colors.black), 
			#El tamaño de las letras de cada una de las celdas será de 10
			('FONTSIZE', (0, 0), (-1, -1), 13),
		]
		))

		# Cerramos limpiamente el objeto PDF.
		p.showPage()
		bandera = False
		contador = 0
		if familia:
			p.setFont("Times-Bold", 19)
			p.drawString(200, 760, u"LISTADO DE FAMILIARES")
			p.drawImage('static/imagenes/logo_pdf.png' , 480, 735, width=75, height=75)
			p.setFont("Helvetica-BoldOblique", 14)
			p.drawString(80, 700, u"Familiares:")
			p.setFont("Times-Italic", 9)
			p.drawString(265,40, "ADVERTENCIA")
			p.drawString(78,30, "El uso de la información almacenada en esta base de datos está limitado a fines eclesiásticos de los miembros del Centro")
			p.drawString(217,20, "Evangelístico Pereira, quedando excluido cualquier otro uso.")
			x = 80
			y = 650
			s = 630
			for iteracion in familia:
				bandera = True
				y-=15
				s-=30
				contador +=1
			if contador > 8 and contador < 15:
				y-=25
			if contador > 14 and contador < 22:
				y-=25
			if contador > 21 and contador < 29:
				y-=25
		if bandera:
				detalle_orden.wrapOn(p, 792, 612)
				#Definimos la coordenada donde se dibujará la tabla
				detalle_orden.drawOn(p, x, y)
				p.showPage()

		p.save()

		# Traemos  el valor de el bufer BytesIO y escribimos la respuesta.
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def index_vistas(request):
	return render(request, 'vistas/index.html')

def Gestion_Miembros(request):
	if request.user.is_superuser:
		return render(request, 'vistas/Gestion_Miembros.html')	
	else:
		return render(request, 'mensajes/error_no_super_user.html') 

def Gestion_Grupos(request):
	return render(request, 'vistas/Gestion_Grupos.html')

class perfil(views.SuperuserRequiredMixin,ListView):
	
	context_object_name = "info_list"
	template_name = 'usuario/perfil_otro_2.html'
	
	def get_queryset(self):
		self.usuario = get_object_or_404(Usuario, id__iexact=self.args[0])
		
		Info = Conyuge_hijos.objects.filter(usuario=self.usuario)

		if Info.exists():
			return Conyuge_hijos.objects.filter(usuario=self.usuario)
		else:
			print(self.usuario)
			return Usuario.objects.filter(nombres=self.usuario.nombres, apellidos=self.usuario.apellidos)
				


	def get_context_data(self, **kwargs):
		context = super(perfil, self).get_context_data(**kwargs)
		context['usuario'] = self.usuario
		return context   


def creacion_conyuge_hijos_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/creacion_conyuge_hijos_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def creacion_usuario_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/creacion_usuario_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def editar_conyuge_hijos_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/editar_conyuge_hijos_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def editar_usuario_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/editar_usuario_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def eliminar_conyuge_hijos_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/eliminacion_conyugehijos_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def eliminar_usuario_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/eliminacion_usuario_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 


def MiembroList(request):
	if request.user.is_superuser:
		template = 'usuario/usuario_buscar.html'
		usuario = Usuario.objects.all().order_by('nombres')

		pages = pagination(request, usuario, num=5)

		context = {
        	'items': pages[0],
        	'page_range': pages[1],
    	}

		return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')

def search(request):
	if request.user.is_superuser:
		template = 'usuario/usuario_buscar.html'

		query = request.GET.get('q')
		if query:
			usuario = Usuario.objects.filter(Q(nombres__icontains=query)|
					Q(apellidos__icontains=query)|
					Q(direccion__icontains=query)|
					Q(barrio__icontains=query)
				).order_by('nombres')
		else:
			usuario = Usuario.objects.all()

		if not usuario.exists():
			query = elimina_tildes(query)
			usuario = Usuario.objects.filter(Q(nombres__icontains=query)|
					Q(apellidos__icontains=query)|
					Q(direccion__icontains=query)|
					Q(barrio__icontains=query)
				).order_by('nombres')

			pages = pagination(request, usuario, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
		else:
			pages = pagination(request, usuario, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')

class UsuarioCreate(views.SuperuserRequiredMixin,CreateView):
	model = Usuario
	template_name = 'usuario/usuario_form.html'
	form_class = UsuarioForm
	success_url = reverse_lazy('usuario:creacion_usuario_exitosa')

class UsuarioDelete(views.SuperuserRequiredMixin,DeleteView):
	model = Usuario
	template_name = 'usuario/usuario_delete.html'
	success_url = reverse_lazy('usuario:eliminado_usuario_exitosa')

class UsuarioUpdate(views.SuperuserRequiredMixin,UpdateView):
	model = Usuario
	form_class = UsuarioForm
	template_name = 'usuario/usuario_edit.html'
	success_url = reverse_lazy('usuario:edicion_usuario_exitosa')

def Conyuge_hijosList(request):
	if request.user.is_superuser:
		template = 'conyuge_hijos/conyuge_hijos_list.html'
		pariente = Conyuge_hijos.objects.all().order_by('usuario')

		pages = pagination(request, pariente, num=5)

		context = {
        	'items': pages[0],
        	'page_range': pages[1],
    	}
		return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')

def pariente_search(request):
	if request.user.is_superuser:
		template = 'conyuge_hijos/conyuge_hijos_list.html'

		query = request.GET.get('q')
		if query:
			pariente = Conyuge_hijos.objects.filter(Q(nombres_familiar__icontains=query)|
					Q(apellidos_familiar__icontains=query)|
					Q(tipo__icontains=query)
				).order_by('usuario')
		else:
			pariente = Conyuge_hijos.objects.all()

		if not pariente.exists():
			query = elimina_tildes(query)
			pariente = Conyuge_hijos.objects.filter(Q(nombres_familiar__icontains=query)|
					Q(apellidos_familiar__icontains=query)|
					Q(tipo__icontains=query)
				).order_by('usuario')

			pages = pagination(request, pariente, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
		else:
			pages = pagination(request, pariente, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')
	
	
def Conyuge_hijosCreate(request,pk):
	if request.method == "POST":
		auxiliar=Conyuge_hijos()
		auxiliar.tipo=request.POST['tipo']
		auxiliar.nombres_familiar=request.POST['nombres_familiar']
		auxiliar.apellidos_familiar=request.POST['apellidos_familiar']
		auxiliar.edad_familiar=request.POST['edad_familiar']
		auxiliar.usuario=get_object_or_404(Usuario, id__iexact=pk)
		auxiliar.save()
		return render(request, 'mensajes/creacion_conyuge_hijos_exitosa.html')
	else:
		auxiliar=Conyuge_hijos()
		pariente=get_object_or_404(Usuario, id__iexact=pk)
	return render(request, 'conyuge_hijos/conyuge_hijos_form_otro.html', {'form':auxiliar, 'pariente':pariente})	


class Conyuge_hijosDelete(views.SuperuserRequiredMixin,DeleteView):
	model = Conyuge_hijos
	template_name = 'conyuge_hijos/conyuge_hijos_delete.html'
	success_url = reverse_lazy('usuario:eliminado_pariente_exitosa')


class Conyuge_hijosUpdate(views.SuperuserRequiredMixin,UpdateView):	
	model = Conyuge_hijos
	form_class = Conyuge_hijosForm
	template_name = 'conyuge_hijos/conyuge_hijos_edit.html'
	success_url = reverse_lazy('usuario:edicion_exitosa')

def Conyuge_hijosListEdit(request):
	if request.user.is_superuser:
		template = 'usuario/usuario_buscar_register_pariente.html'
		usuario = Usuario.objects.all().order_by('nombres')

		pages = pagination(request, usuario, num=5)

		context = {
        	'items': pages[0],
        	'page_range': pages[1],
    	}

		return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')

def pariente_edit_search(request):
	if request.user.is_superuser:
		template = 'usuario/usuario_buscar_register_pariente.html'

		query = request.GET.get('q')
		if query:
			usuario = Usuario.objects.filter(Q(nombres__icontains=query)|
					Q(apellidos__icontains=query)|
					Q(direccion__icontains=query)|
					Q(barrio__icontains=query)
				).order_by('nombres')
		else:
			usuario = Usuario.objects.all()

		if not usuario.exists():
			query = elimina_tildes(query)
			usuario = Usuario.objects.filter(Q(nombres__icontains=query)|
					Q(apellidos__icontains=query)|
					Q(direccion__icontains=query)|
					Q(barrio__icontains=query)
				).order_by('nombres')

			pages = pagination(request, usuario, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
		else:
			pages = pagination(request, usuario, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}
			return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')