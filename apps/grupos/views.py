from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core import serializers
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.views.generic import View
from django.shortcuts import get_object_or_404
import unicodedata

from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib.pagesizes import A4

from django.db.models import Q
from apps.usuario.config import pagination

from apps.grupos.models import Grupos
from apps.grupos.forms import GruposForm

def pdf_grupos_view(self,pk):
	# Obtenemos un queryset, para un determinado usuario usando pk.
	try:
		grupos = Grupos.objects.get(id=pk)

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
	doc = SimpleDocTemplate("my_doc.pdf", pagesize=letter)

	# Dibujamos cosas en el PDF. Aqui se genera el PDF.
	# Consulta la documentación de ReportLab para una lista completa de funcionalidades.

	centrar=getSampleStyleSheet()
	centrar.add(ParagraphStyle(name = "Titulo",  alignment=TA_CENTER, fontSize=15, fontName="Times-Roman"))
	titulo = Paragraph("REPORTE LIDER DE GRUPO ", centrar['Titulo'])
	Story.append(titulo)
	doc.build(Story)
	titulo.drawOn(p, 70, 760)

	justificacion=getSampleStyleSheet()
	justificacion.add(ParagraphStyle(name = "justificacion",  alignment=TA_JUSTIFY, fontSize=13, fontName="Times-Roman"))

	p.drawImage('static/imagenes/logo_pdf.png' , 480, 735, width=75, height=75)
	
	p.setFont("Helvetica-BoldOblique", 13)
	p.drawString(65, 700, "Fecha de visita:")
	p.setFont("Times-Roman", 13)
	p.drawString(180, 700, " " + str(grupos.fecha_visita))
	p.setFont("Helvetica-BoldOblique", 13)
	p.drawString(360, 700, "Nro. del grupo:")
	p.setFont("Times-Roman", 13)
	p.drawString(460, 700, " " + str(grupos.nro_grupo))
	p.setFont("Helvetica-BoldOblique", 13)
	p.drawString(65, 680, "Lider del grupo:")
	p.setFont("Times-Roman", 13)
	p.drawString(180, 680, " " + str(grupos.lider))
	p.setFont("Helvetica-BoldOblique", 13)
	p.drawString(65, 660, "Supervisor:")
	p.setFont("Times-Roman", 13)
	p.drawString(180, 660, " " + str(grupos.supervisor))

	segundo_titulo = Paragraph("INFORMACIÓN DEL REPORTE", centrar['Titulo'])
	Story.append(segundo_titulo)
	doc.build(Story)
	segundo_titulo.drawOn(p, 70, 605)
	p.setFont("Times-Italic", 13)
	p.drawString(65, 565, "DATOS DEL GRUPO")
	p.drawString(90, 545, "FAMILIAR:")
	p.setFont("Times-Roman", 13)
	p.drawString(75, 520, "Hermanos:")
	p.drawString(140, 520, " " + str(grupos.hermanos_familiar))
	p.drawString(75, 500, "Discípulos:")
	p.drawString(140, 500, " " + str(grupos.discipulos_familiar))
	p.drawString(75, 480, "Amigos:")
	p.drawString(140, 480, " " + str(grupos.amigos_familiar))
	p.drawString(75, 460, "Niños cristianos:")
	p.drawString(170, 460, " " + str(grupos.niños_cristianos))
	p.drawString(75, 440, "Niños amigos:")
	p.drawString(160, 440, " " + str(grupos.niños_amigos))
	p.drawString(75, 420, "Conversiones:")
	p.drawString(160, 420, " " + str(grupos.conversiones_familiar))
	p.drawString(75, 400, "Conversiones niños:")
	p.drawString(180, 400, " " + str(grupos.conversiones_niños))

	p.setFont("Times-Italic", 13)
	p.drawString(245, 565, "DATOS DEL PDI-")
	p.drawString(265, 545, "VISITAS:")
	p.setFont("Times-Roman", 13)
	p.drawString(255, 520, "Telefónica:")
	p.drawString(315, 520, " " + str(grupos.telefonica))
	p.drawString(255, 500, "Electrónica:")
	p.drawString(315, 500, " " + str(grupos.electronica))
	p.drawString(255, 480, "Personal:")
	p.drawString(315, 480, " " + str(grupos.personal))
	p.drawString(255, 460, "Esc. de capacitación:")
	p.drawString(365, 460, " " + str(grupos.esc_capacitacion))

	p.setFont("Times-Italic", 13)
	p.drawString(440, 565, "DATOS")
	p.drawString(435, 545, "IGLESIA:")
	p.setFont("Times-Roman", 13)
	p.drawString(425, 520, "Hermanos:")
	p.drawString(495, 520, " " + str(grupos.hermanos_iglesia))
	p.drawString(425, 500, "Discípulos:")
	p.drawString(495, 500, " " + str(grupos.discipulos_iglesia))
	p.drawString(425, 480, "Amigos:")
	p.drawString(495, 480, " " + str(grupos.amigos_iglesia))
	p.drawString(425, 460, "Niños:")
	p.drawString(495, 460, " " + str(grupos.niños_iglesia))
	p.drawString(425, 440, "Conversiones:")
	p.drawString(505, 440, " " + str(grupos.conversiones_iglesia))

	p.drawString(75, 350, "Ofrenda del grupo:")
	p.drawString(200, 350, " " + str(grupos.ofrenda_grupo))

	tercer_titulo = Paragraph("FALTARON AL GRUPO", centrar['Titulo'])
	Story.append(tercer_titulo)
	doc.build(Story)
	tercer_titulo.drawOn(p, 70, 290)
	p.setFont("Times-Italic", 13)
	p.drawString(75, 250, "Persona")
	p.drawString(290, 250, "Motivo")
	p.drawString(440, 250, "Visitó Después")
	p.setFont("Times-Roman", 13)

	mensaje = 0
	if grupos.faltaron_grupo_uno:
		p.drawString(75, 230, " " + str(grupos.faltaron_grupo_uno))
		p.drawString(290, 230, " " + str(grupos.motivo_grupo_uno))
		p.drawString(465, 230, " " + str(grupos.visito_despues_uno))
	else:
		mensaje+=1

	if grupos.faltaron_grupo_dos:
		p.drawString(75, 200, " " + str(grupos.faltaron_grupo_dos))
		p.drawString(290, 200, " " + str(grupos.motivo_grupo_dos))
		p.drawString(465, 200, " " + str(grupos.visito_despues_dos))
	else:
		mensaje+=1

	if grupos.faltaron_grupo_tres:
		p.drawString(75, 170, " " + str(grupos.faltaron_grupo_tres))
		p.drawString(290, 170, " " + str(grupos.motivo_grupo_tres))
		p.drawString(465, 170, " " + str(grupos.visito_despues_tres))
	else:
		mensaje+=1

	if grupos.faltaron_grupo_cuatro:
		p.drawString(75, 140, " " + str(grupos.faltaron_grupo_cuatro))
		p.drawString(290, 140, " " + str(grupos.motivo_grupo_cuatro))
		p.drawString(465, 140, " " + str(grupos.visito_despues_cuatro))
	else:
		mensaje+=1

	if grupos.faltaron_grupo_cinco:
		p.drawString(75, 110, " " + str(grupos.faltaron_grupo_cinco))
		p.drawString(290, 110, " " + str(grupos.motivo_grupo_cinco))
		p.drawString(465, 110, " " + str(grupos.visito_despues_cinco))
	else:
		mensaje+=1

	if mensaje == 5:
		centro_mensaje=getSampleStyleSheet()
		centro_mensaje.add(ParagraphStyle(name = "Titulo",  alignment=TA_CENTER, fontSize=13, fontName="Times-Roman"))
		titulo_mensaje = Paragraph("No se presentó inasistencia", centro_mensaje['Titulo'])
		Story.append(titulo_mensaje)
		doc.build(Story)
		titulo_mensaje.drawOn(p, 70, 190)
	p.showPage()

	convertidos_y = 0
	comentarios_y = 0

	if grupos.nuevos_convertidos:
		cadena_convertidos = str(grupos.nuevos_convertidos)
		
		p.setFont("Times-Italic", 13)
		cuarto_titulo = Paragraph("NUEVOS CONVERTIDOS", centrar['Titulo'])
		Story.append(cuarto_titulo)
		doc.build(Story)
		cuarto_titulo.drawOn(p, 65, 730)

		if len(cadena_convertidos)<150:
			convertidos_y = 700

		if len(cadena_convertidos)>149:
			convertidos_y = 670

		new_convertidos = Paragraph(" " +str(grupos.nuevos_convertidos), justificacion['justificacion'])
		Story.append(new_convertidos)
		doc.build(Story)
		new_convertidos.drawOn(p, 65, convertidos_y)

		if grupos.comentarios:
			p.drawImage('static/imagenes/logo_pdf.png' , 480, 735, width=75, height=75)
			quinto_titulo = Paragraph("COMENTARIOS", centrar['Titulo'])
			Story.append(quinto_titulo)
			doc.build(Story)
			quinto_titulo.drawOn(p, 65, 620)

			cadena_comentarios = str(grupos.comentarios)

			if len(cadena_comentarios)<150:
				comentarios_y = 590

			if len(cadena_comentarios)>149:
				comentarios_y = 560

			if len(cadena_comentarios)>299 and len(cadena_comentarios)<450:
				comentarios_y = 530


			comentario = Paragraph(" " +str(grupos.comentarios), justificacion['justificacion'])
			Story.append(comentario)
			doc.build(Story)
			comentario.drawOn(p, 65, comentarios_y)
			p.showPage()
		else:
			p.drawImage('static/imagenes/logo_pdf.png' , 480, 735, width=75, height=75)
			p.showPage()

	elif grupos.comentarios:
		p.drawImage('static/imagenes/logo_pdf.png' , 480, 735, width=75, height=75)
		quinto_titulo = Paragraph("COMENTARIOS", centrar['Titulo'])
		Story.append(quinto_titulo)
		doc.build(Story)
		quinto_titulo.drawOn(p, 65, 730)

		cadena_comentarios = str(grupos.comentarios)

		if len(cadena_comentarios)<150:
			comentarios_y = 700

		if len(cadena_comentarios)>149 and len(cadena_comentarios)<300:
			comentarios_y = 670

		if len(cadena_comentarios)>299 and len(cadena_comentarios)<450:
			comentarios_y = 640

		comentario = Paragraph(" " +str(grupos.comentarios), justificacion['justificacion'])
		Story.append(comentario)
		doc.build(Story)
		comentario.drawOn(p, 65, comentarios_y)	
		p.showPage()

	
	p.save()

	# Traemos  el valor de el bufer BytesIO y escribimos la respuesta.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response

def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def editar_grupos_exitosa(request):
	return render(request, 'mensajes/editar_grupos_exitosa.html')

def eliminacion_grupos_exitosa(request):
	return render(request, 'mensajes/eliminacion_grupos_exitosa.html')

def creacion_grupos_exitosa(request):
	return render(request, 'mensajes/creacion_grupos_exitosa.html')

class Info(ListView):
	context_object_name = "info_list"
	template_name = 'grupos/info_grupo.html'

	def get_queryset(self):
		self.usuario = get_object_or_404(Grupos, id__iexact=self.args[0])
		return Grupos.objects.filter(lider=self.usuario.lider)
			

	def get_context_data(self, **kwargs):
		context = super(Info, self).get_context_data(**kwargs)
		context['usuario'] = self.usuario
		return context

def GruposList(request):
	template = 'grupos/grupos_buscar.html'
	grupos = Grupos.objects.all().order_by('-fecha_visita')

	pages = pagination(request, grupos, num=2)

	context = {
		'items': pages[0],
    	'page_range': pages[1],
	}

	return render(request, template, context)

def grupo_search(request):
	template = 'grupos/grupos_buscar.html'

	query = request.GET.get('q')
	if query:
		grupos = Grupos.objects.filter(Q(nro_grupo__icontains=query)|
				Q(lider__icontains=query)|
				Q(supervisor__icontains=query)
			).order_by('-fecha_visita')
	else:
		grupos = Grupos.objects.all()

	if not grupos.exists():
		query = elimina_tildes(query)
		grupos = Grupos.objects.filter(Q(nro_grupo__icontains=query)|
				Q(lider__icontains=query)|
				Q(supervisor__icontains=query)
			).order_by('-fecha_visita')
		pages = pagination(request, grupos, num=2)
		context = {
			'items': pages[0],
   			'page_range': pages[1],
   			'query': query,
		}	
		return render(request, template, context)
	else:
		pages = pagination(request, grupos, num=2)
		context = {
			'items': pages[0],
   			'page_range': pages[1],
   			'query': query,
		}	
		return render(request, template, context)

class GruposCreate(CreateView):
	model = Grupos
	template_name = 'grupos/grupos_formulario.html'
	form_class = GruposForm
	success_url = reverse_lazy('grupos:creacion_exitosa')
	
class GruposDelete(DeleteView):
	model = Grupos
	template_name = 'grupos/grupos_delete.html'
	success_url = reverse_lazy('grupos:eliminacion_exitosa')

class GruposUpdate(UpdateView):
	model = Grupos
	template_name = 'grupos/grupos_edit.html'
	form_class = GruposForm
	success_url = reverse_lazy('grupos:edicion_exitosa')

def graficaAnio(request):
	if request.user.is_superuser:

		template = loader.get_template('grupos/graficaAnio.html')

		if request.method == 'POST':
			flag = True
			template = loader.get_template('grupos/graficaAnio.html')
			anio = request.POST.get("value2")
			numgrupo = request.POST.get("value1")
			tipovisita = request.POST.get("visita")

			if anio and numgrupo and tipovisita:
		
				datos = Grupos.objects.all()
				color=[]
				mes=[0]*12

				if int(tipovisita)==1:
					texto="Hermanos"
				if int(tipovisita)==2:
					texto="Discípulos"
				if int(tipovisita)==3:
					texto="Amigos"
				if int(tipovisita)==4:
					texto="Niños Cristiano"
				if int(tipovisita)==5:
					texto="Niños Amigos"
				if int(tipovisita)==6:
					texto="Conversiones"
				if int(tipovisita)==7:
					texto="Conversiones Niños"
				if int(tipovisita)==8:
					texto="Telefónica"	
				if int(tipovisita)==9:
					texto="Electrónica"	
				if int(tipovisita)==10:
					texto="Personal"	
				if int(tipovisita)==11:
					texto="Esc. de Capacitación"	
				if int(tipovisita)==12:
					texto="Hermanos"	
				if int(tipovisita)==13:
					texto="Discípulos"	
				if int(tipovisita)==14:
					texto="Amigos"	
				if int(tipovisita)==15:
					texto="Niños"	
				if int(tipovisita)==16:
					texto="Conversiones"
				if int(tipovisita)==17:
					texto="Ofrendas"																

				info=("Información de "+str(texto)+" del grupo "+str(numgrupo)+" en el año "+str(anio))

				nombre=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
				i = 0
				for contador in range(11):

					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i +=1


				for item in datos:

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(1):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.hermanos_familiar
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.hermanos_familiar
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.hermanos_familiar
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.hermanos_familiar
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.hermanos_familiar
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.hermanos_familiar
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.hermanos_familiar
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.hermanos_familiar
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.hermanos_familiar
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.hermanos_familiar
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.hermanos_familiar
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.hermanos_familiar

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(2):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.discipulos_familiar
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.discipulos_familiar
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.discipulos_familiar
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.discipulos_familiar
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.discipulos_familiar
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.discipulos_familiar
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.discipulos_familiar
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.discipulos_familiar
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.discipulos_familiar
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.discipulos_familiar
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.discipulos_familiar
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.discipulos_familiar

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(3):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.amigos_familiar
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.amigos_familiar
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.amigos_familiar
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.amigos_familiar
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.amigos_familiar
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.amigos_familiar
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.amigos_familiar
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.amigos_familiar
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.amigos_familiar
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.amigos_familiar
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.amigos_familiar
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.amigos_familiar

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(4):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.niños_cristianos
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.niños_cristianos
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.niños_cristianos
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.niños_cristianos
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.niños_cristianos
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.niños_cristianos
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.niños_cristianos
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.niños_cristianos
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.niños_cristianos
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.niños_cristianos
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.niños_cristianos
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.niños_cristianos

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(5):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.niños_amigos
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.niños_amigos
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.niños_amigos
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.niños_amigos
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.niños_amigos
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.niños_amigos
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.niños_amigos
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.niños_amigos
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.niños_amigos
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.niños_amigos
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.niños_amigos
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.niños_amigos

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(6):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.conversiones_familiar
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.conversiones_familiar
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.conversiones_familiar
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.conversiones_familiar
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.conversiones_familiar
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.conversiones_familiar
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.conversiones_familiar
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.conversiones_familiar
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.conversiones_familiar
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.conversiones_familiar
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.conversiones_familiar
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.conversiones_familiar

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(7):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.conversiones_niños
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.conversiones_niños
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.conversiones_niños
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.conversiones_niños
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.conversiones_niños
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.conversiones_niños
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.conversiones_niños
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.conversiones_niños
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.conversiones_niños
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.conversiones_niños
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.conversiones_niños
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.conversiones_niños	

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(8):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.telefonica
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.telefonica
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.telefonica
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.telefonica
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.telefonica
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.telefonica
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.telefonica
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.telefonica
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.telefonica
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.telefonica
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.telefonica
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.telefonica

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(9):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.electronica
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.electronica
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.electronica
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.electronica
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.electronica
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.electronica
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.electronica
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.electronica
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.electronica
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.electronica
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.electronica
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.electronica

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(10):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.personal
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.personal
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.personal
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.personal
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.personal
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.personal
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.personal
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.personal
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.personal
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.personal
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.personal
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.personal
					
					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(11):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.esc_capacitacion
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.esc_capacitacion
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.esc_capacitacion
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.esc_capacitacion
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.esc_capacitacion
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.esc_capacitacion
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.esc_capacitacion
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.esc_capacitacion
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.esc_capacitacion
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.esc_capacitacion
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.esc_capacitacion
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.esc_capacitacion

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(12):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.hermanos_iglesia
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.hermanos_iglesia
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.hermanos_iglesia
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.hermanos_iglesia
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.hermanos_iglesia
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.hermanos_iglesia
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.hermanos_iglesia
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.hermanos_iglesia
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.hermanos_iglesia
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.hermanos_iglesia
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.hermanos_iglesia
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.hermanos_iglesia

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(13):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.discipulos_iglesia
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.discipulos_iglesia
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.discipulos_iglesia
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.discipulos_iglesia
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.discipulos_iglesia
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.discipulos_iglesia
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.discipulos_iglesia
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.discipulos_iglesia
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.discipulos_iglesia
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.discipulos_iglesia
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.discipulos_iglesia
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.discipulos_iglesia
					
					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(14):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.amigos_iglesia
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.amigos_iglesia
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.amigos_iglesia
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.amigos_iglesia
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.amigos_iglesia
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.amigos_iglesia
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.amigos_iglesia
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.amigos_iglesia
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.amigos_iglesia
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.amigos_iglesia
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.amigos_iglesia
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.amigos_iglesia	

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(15):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.niños_iglesia
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.niños_iglesia
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.niños_iglesia
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.niños_iglesia
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.niños_iglesia
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.niños_iglesia
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.niños_iglesia
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.niños_iglesia
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.niños_iglesia
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.niños_iglesia
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.niños_iglesia
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.niños_iglesia

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(16):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.conversiones_iglesia
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.conversiones_iglesia
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.conversiones_iglesia
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.conversiones_iglesia
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.conversiones_iglesia
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.conversiones_iglesia
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.conversiones_iglesia
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.conversiones_iglesia
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.conversiones_iglesia
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.conversiones_iglesia
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.conversiones_iglesia
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.conversiones_iglesia

					if item.fecha_visita.year == int(anio) and item.nro_grupo == int(numgrupo) and int(tipovisita)==int(17):
					
						if int(item.fecha_visita.month) == int(1) :
							mes[0] = mes[0] + item.ofrenda_grupo
						elif item.fecha_visita.month == 2 :
							mes[1] = mes[1] + item.ofrenda_grupo
						elif item.fecha_visita.month == 3 :
							mes[2] = mes[2] + item.ofrenda_grupo
						elif int(item.fecha_visita.month) == int(4) :
							mes[3] = mes[3] + item.ofrenda_grupo
						elif item.fecha_visita.month == 5 :
							mes[4] = mes[4] + item.ofrenda_grupo
						elif item.fecha_visita.month == 6 :
							mes[5] = mes[5] + item.ofrenda_grupo
						elif item.fecha_visita.month == 7 :
							mes[6] = mes[6] + item.ofrenda_grupo
						elif item.fecha_visita.month == 8 :
							mes[7] = mes[7] + item.ofrenda_grupo
						elif item.fecha_visita.month == 9 :
							mes[8] = mes[8] + item.ofrenda_grupo
						elif item.fecha_visita.month == 10 :
							mes[9] = mes[9] + item.ofrenda_grupo
						elif item.fecha_visita.month == 11 :
							mes[10] = mes[10] + item.ofrenda_grupo
						elif item.fecha_visita.month == 12 :
							mes[11] = mes[11] + item.ofrenda_grupo																											

					#color = simplejson.dumps(color)
					#nombre=simplejson.dumps(nombre)
					#mes=simplejson.dumps(mes)	

				context={
					'info':info,
					'mes':mes,
					'color':color,
					'nombre':nombre,
					'i':i,	
					'flag' : flag,
				}
				return HttpResponse(template.render(context,request))

		if request.method == 'GET':
			flag = False
			datos = []
			color=[]
			info=" "
			mes=[0]*12

			nombre=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
			i = 0
			template = loader.get_template('grupos/graficaAnio.html')
			context={
					'info':info,
					'mes':mes,
					'color':color,
					'nombre':nombre,
					'i':i,	
					'flag' : flag,
				}
			return HttpResponse(template.render(context,request))	
	else:
		return render(request, 'mensajes/error_no_super_user.html') 

def graficaMes(request):
	if request.user.is_superuser:
		template = loader.get_template('grupos/graficaMes.html')
		meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		
		if request.method == 'POST':
			flag = True
			template = loader.get_template('grupos/graficaMes.html')
			numgrupo = request.POST.get("value1") #Grupo
			mesSelect = request.POST.get("value2") #Mes
			anio = request.POST.get("value3") #Anio
			tipovisita = request.POST.get("visita")

			if int(tipovisita)==1:
					texto="Hermanos"
			if int(tipovisita)==2:
				texto="Discípulos"
			if int(tipovisita)==3:
				texto="Amigos"
			if int(tipovisita)==4:
				texto="Niños Cristiano"
			if int(tipovisita)==5:
				texto="Niños Amigos"
			if int(tipovisita)==6:
				texto="Conversiones"
			if int(tipovisita)==7:
				texto="Conversiones Niños"
			if int(tipovisita)==8:
				texto="Telefónica"	
			if int(tipovisita)==9:
				texto="Electrónica"	
			if int(tipovisita)==10:
				texto="Personal"	
			if int(tipovisita)==11:
				texto="Esc. de Capacitación"	
			if int(tipovisita)==12:
				texto="Hermanos"	
			if int(tipovisita)==13:
				texto="Discípulos"	
			if int(tipovisita)==14:
				texto="Amigos"	
			if int(tipovisita)==15:
				texto="Niños"	
			if int(tipovisita)==16:
				texto="Conversiones"
			if int(tipovisita)==17:
				texto="Ofrendas"																

			info=("Información de "+str(texto)+" del grupo "+str(numgrupo)+" del mes "+str(mesSelect)+" en el año "+str(anio))

			value4=0
			if mesSelect.lower()=="enero":
				value4=1
			else:
				if mesSelect.lower()=="febrero":
					value4=2
				else:
					if mesSelect.lower()=="marzo":
						value4=3	
					else:
						if mesSelect.lower()=="abril":
							value4=4
						else:
							if mesSelect.lower()=="mayo":
								value4=5
							else:
								if mesSelect.lower()=="junio":
									value4=6
								else:
									if mesSelect.lower()=="julio":
										value4=7
									else:
										if mesSelect.lower()=="agosto":
											value4=8
										else:
											if mesSelect.lower()=="septiembre":
												value4=9
											else:
												if mesSelect.lower()=="octubre":
													value4=10
												else:
													if mesSelect.lower()=="noviembre":
														value4=11
													else:
														if mesSelect.lower()=="diciembre":
															value4=12							

				
			

			datos = Grupos.objects.all()

			i = 0
			color=[]
			mes=[]

			nombre=[]
			
			for item in datos:

				if item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) and int(tipovisita)==1 :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.hermanos_familiar)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) and int(tipovisita)==2 :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.discipulos_familiar)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==3 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.amigos_familiar)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==4 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.niños_cristianos)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==5 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.niños_amigos)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==6 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.conversiones_familiar)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==7 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.conversiones_niños)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==8 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.telefonica)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==9 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.electronica)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==10 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.personal)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==11 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.esc_capacitacion)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==12 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.hermanos_iglesia)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==13 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.discipulos_iglesia)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==14 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.amigos_iglesia)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==15 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.niños_iglesia)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==16 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.conversiones_iglesia)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				

				if  int(tipovisita)==17 and item.fecha_visita.year == int(anio) and item.fecha_visita.month == int(value4) and item.nro_grupo == int(numgrupo) :
					
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1
					mes.append(item.ofrenda_grupo)							
					nombre.append(str(item.fecha_visita.day)+" "+meses[item.fecha_visita.month-1])				




					

			context={
				'info':info,
				'mes':mes,
				'color':color,
				'nombre':nombre,
				'i':i,	
				
			}
			return HttpResponse(template.render(context,request))

		if request.method == 'GET':
			flag = False
			datos = []
			color=[]
			mes=[0]*12
			info=" "

			nombre=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
			i = 0
			template = loader.get_template('grupos/graficaMes.html')
			context={
					'info':info,
					'mes':mes,
					'color':color,
					'nombre':nombre,
					'i':i,	
					'flag' : flag,
				}
			return HttpResponse(template.render(context,request))	
	else:
		return render(request, 'mensajes/error_no_super_user.html') 			