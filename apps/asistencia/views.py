from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views.generic import View
import re
from django.shortcuts import render_to_response
from apps.asistencia.models import Asistencia
from apps.asistencia.forms import AsistenciaForm

from apps.usuario.config import pagination
from django.db.models import Q
import unicodedata

from datetime import time, date
import json as simplejson
import random

from django.views.generic import TemplateView
from mixin import Mixin, mixin
from braces import views

def elimina_tildes(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def grafica(request):
	if request.user.is_superuser: 
		return render(request, 'asistencia/grafica.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 


def graficaAnio(request):
	if request.user.is_superuser:

		template = loader.get_template('asistencia/grafica_anio.html')

		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_anio.html')
			value = request.POST.get("value")

			if value:
		
				datos = Asistencia.objects.all()
				color=[]
				mes=[0]*12
				info=("Información del año "+str(value))

				nombre=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
				i = 0
				for contador in range(11):

					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i +=1


				for item in datos:

					if item.fecha_registro.year == int(value):
					
						if int(item.fecha_registro.month) == int(1) :
							mes[0] = mes[0] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 2 :
							mes[1] = mes[1] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes	
						elif item.fecha_registro.month == 3 :
							mes[2] = mes[2] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif int(item.fecha_registro.month) == int(4) :
							mes[3] = mes[3] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 5 :
							mes[4] = mes[4] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes	
						elif item.fecha_registro.month == 6 :
							mes[5] = mes[5] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 7 :
							mes[6] = mes[6] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 8 :
							mes[7] = mes[7] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 9 :
							mes[8] = mes[8] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes
						elif item.fecha_registro.month == 10 :
							mes[9] = mes[9] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes	
						elif item.fecha_registro.month == 11 :
							mes[10] = mes[10] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes	
						elif item.fecha_registro.month == 12 :
							mes[11] = mes[11] + item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes							


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
			template = loader.get_template('asistencia/grafica_anio.html')
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
		template = loader.get_template('asistencia/grafica_mes.html')
		meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		
		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_mes.html')
			value1 = request.POST.get("value1") #Mes
			value2 = request.POST.get("value2") #Anio

			info=("Información del mes "+str(value1)+" del año "+str(value2))

			if value1.lower()=="enero":
				value1=1
			else:
				if value1.lower()=="febrero":
					value1=2
				else:
					if value1.lower()=="marzo":
						value1=3	
					else:
						if value1.lower()=="abril":
							value1=4
						else:
							if value1.lower()=="mayo":
								value1=5
							else:
								if value1.lower()=="junio":
									value1=6
								else:
									if value1.lower()=="julio":
										value1=7
									else:
										if value1.lower()=="agosto":
											value1=8
										else:
											if value1.lower()=="septiembre":
												value1=9
											else:
												if value1.lower()=="octubre":
													value1=10
												else:
													if value1.lower()=="noviembre":
														value1=11
													else:
														if value1.lower()=="diciembre":
															value1=12							

				
			if value1 and value2:

				datos = Asistencia.objects.all()

				i = 0
				color=[]
				mes=[]

				nombre=[]
				
				for item in datos:

					if item.fecha_registro.year == int(value2) and item.fecha_registro.month == int(value1):
						
						r = lambda: random.randint(0,255)
						r = lambda: random.randint(0,255)
						color.append('#%02X%02X%02X' % (r(),r(),r()))
						i+=1


						mes.append(item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes)
						dia=item.dia[0]+item.dia[1]+item.dia[2]+"."
							
						nombre.append(dia+" "+str(item.fecha_registro.day)+" "+meses[item.fecha_registro.month-1])				

					#color = simplejson.dumps(color)
					#nombre=simplejson.dumps(nombre)
					#mes=simplejson.dumps(mes)	

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
			template = loader.get_template('asistencia/grafica_mes.html')
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

def graficaSemana(request):
	if request.user.is_superuser:
		template = loader.get_template('asistencia/grafica_semana.html')
		meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		
		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_semana.html')
			value0 = request.POST.get("value0") #Semana
			value1 = request.POST.get("value1") #Mes
			value2 = request.POST.get("value2") #Anio
			info=("Información de la Semana # "+str(value0)+" del mes "+str(value1)+" del año "+str(value2))
			
			if value1.lower()=="enero":
				value1=1
			else:
				if value1.lower()=="febrero":
					value1=2
				else:
					if value1.lower()=="marzo":
						value1=3	
					else:
						if value1.lower()=="abril":
							value1=4
						else:
							if value1.lower()=="mayo":
								value1=5
							else:
								if value1.lower()=="junio":
									value1=6
								else:
									if value1.lower()=="julio":
										value1=7
									else:
										if value1.lower()=="agosto":
											value1=8
										else:
											if value1.lower()=="septiembre":
												value1=9
											else:
												if value1.lower()=="octubre":
													value1=10
												else:
													if value1.lower()=="noviembre":
														value1=11
													else:
														if value1.lower()=="diciembre":
															value1=12							



			if value1 and value2 and value0:

				datos = Asistencia.objects.all().order_by("fecha_registro")

				i = 0
				color=[]
				mes=[]

				nombre=[]

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				value0=int(value0) #Semana
				value1=int(value1) #Mes
				value2=int(value2) #Anio

				if int(value1) == 1:
					value3=12
					value5=value2-1
				else:
					value3=int(value1)-1	
					value5=value2
				
				cont=0
				cont2=0
				dia_anterior="0"
				for item in datos:

					if item.fecha_registro.year == int(value2) and item.fecha_registro.month == int(value1):
						
						#if cont==1 and item.dia=="Miercoles":
						#	cont=2

						if dia_anterior ==  item.dia:
							cont+=1
							cont2+=1


						if value0 == 1 and item.dia.lower() == "miercoles" and cont==0 and cont2==0:

							for item1 in datos:
								if item1.fecha_registro.year == int(value5) and item1.fecha_registro.month == int(value3):
									mes1=(item1.asistencia_hombres + item1.asistencia_mujeres + item1.asistencia_niños +item1.asistencia_jovenes + item1.asistencia_adolecentes)
									dia=item1.dia[0]+item1.dia[1]+item1.dia[2]+"."
							
									nombre1=(dia+" "+str(item1.fecha_registro.day)+" "+meses[value3-1]+" del "+str(value5))				
							mes.append(mes1)
							mes.append(item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes)
							dia=item.dia[0]+item.dia[1]+item.dia[2]+"."
							nombre.append(nombre1)
							nombre.append(dia+" "+str(item.fecha_registro.day)+" "+meses[item.fecha_registro.month-1])		
							cont=2	
							cont2=2	
							break

						if value0-1 == cont//2 :		
							cont2+=1
							mes.append(item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes)
							dia=item.dia[0]+item.dia[1]+item.dia[2]+"."
							nombre.append(dia+" "+str(item.fecha_registro.day)+" "+meses[item.fecha_registro.month-1])				
							cont=cont-1
							if cont2==2:
								break
						cont+=1		

						dia_anterior=item.dia

					#color = simplejson.dumps(color)
					#nombre=simplejson.dumps(nombre)
					#mes=simplejson.dumps(mes)	
				if value1==12:
					value3=1
					value4=value2+1
				else:
					value3=value1+1
					value4=value2	


				

				if cont2==1:
					for item in datos:
						if item.fecha_registro.year == int(value4) and item.fecha_registro.month == int(value3):
							mes.append(item.asistencia_hombres + item.asistencia_mujeres + item.asistencia_niños +item.asistencia_jovenes + item.asistencia_adolecentes)
							dia=item.dia[0]+item.dia[1]+item.dia[2]+"."
							nombre.append(dia+" "+str(item.fecha_registro.day)+" "+meses[item.fecha_registro.month-1])				
							break
					


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
			template = loader.get_template('asistencia/grafica_semana.html')
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

def TiposgraficaAnio(request):
	if request.user.is_superuser:
		template = loader.get_template('asistencia/grafica_anio_tipo.html')

		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_anio_tipo.html')
			value = request.POST.get("value")
			info=("Información del año "+str(value))

			if value:
		
				datos = Asistencia.objects.all()
				color=[]
				mes=[0]*5

				nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]
				i = 0
				for contador in range(5):

					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i +=1


				for item in datos:

					if item.fecha_registro.year == int(value):
					
						if int(item.fecha_registro.month) == int(1) :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños  
						elif item.fecha_registro.month == 2 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 3 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif int(item.fecha_registro.month) == int(4) :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 5 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 6 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 7 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 8 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 9 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 10 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 11 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 
						elif item.fecha_registro.month == 12 :
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños 


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
			mes=[0]*12
			info=" "
			nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]
			i = 0
			template = loader.get_template('asistencia/grafica_anio_tipo.html')
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

def TiposgraficaMes(request):
	if request.user.is_superuser:
		template = loader.get_template('asistencia/grafica_mes_tipo.html')
		mes=[0]*5
		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_mes_tipo.html')
			value1 = request.POST.get("value1") #Mes
			value2 = request.POST.get("value2") #Anio
			info=("Información del mes "+str(value1)+" del año "+str(value2))

			if value1.lower()=="enero":
				value1=1
			else:
				if value1.lower()=="febrero":
					value1=2
				else:
					if value1.lower()=="marzo":
						value1=3	
					else:
						if value1.lower()=="abril":
							value1=4
						else:
							if value1.lower()=="mayo":
								value1=5
							else:
								if value1.lower()=="junio":
									value1=6
								else:
									if value1.lower()=="julio":
										value1=7
									else:
										if value1.lower()=="agosto":
											value1=8
										else:
											if value1.lower()=="septiembre":
												value1=9
											else:
												if value1.lower()=="octubre":
													value1=10
												else:
													if value1.lower()=="noviembre":
														value1=11
													else:
														if value1.lower()=="diciembre":
															value1=12							

				
			if value1 and value2:

				datos = Asistencia.objects.all()

				i = 0
				color=[]

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1

				r = lambda: random.randint(0,255)
				r = lambda: random.randint(0,255)
				color.append('#%02X%02X%02X' % (r(),r(),r()))
				i+=1
				
				mes=[0]*5			
				nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]
				for item in datos:

					if item.fecha_registro.year == int(value2) and item.fecha_registro.month == int(value1):
						
						


						mes[0] = mes[0] + item.asistencia_hombres 
						mes[1] = mes[1] + item.asistencia_mujeres 
						mes[2] = mes[2] + item.asistencia_adolecentes 
						mes[3] = mes[3] + item.asistencia_jovenes 
						mes[4] = mes[4] + item.asistencia_niños  
							
						
					#color = simplejson.dumps(color)
					#nombre=simplejson.dumps(nombre)
					#mes=simplejson.dumps(mes)	

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
			mes=[0]*5
			info=" "
			nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]
			i = 0
			template = loader.get_template('asistencia/grafica_mes_tipo.html')
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

def TiposgraficaSemana(request): 
	if request.user.is_superuser:
		template = loader.get_template('asistencia/grafica_semana_tipo.html')
		meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		
		if request.method == 'POST':
			flag = True
			template = loader.get_template('asistencia/grafica_semana_tipo.html')
			value0 = request.POST.get("value0") #Semana
			value1 = request.POST.get("value1") #Mes
			value2 = request.POST.get("value2") #Anio
			info=("Información de la Semana # "+str(value0)+" del mes "+str(value1)+" del año "+str(value2))
			
			if value1.lower()=="enero":
				value1=1
			else:
				if value1.lower()=="febrero":
					value1=2
				else:
					if value1.lower()=="marzo":
						value1=3	
					else:
						if value1.lower()=="abril":
							value1=4
						else:
							if value1.lower()=="mayo":
								value1=5
							else:
								if value1.lower()=="junio":
									value1=6
								else:
									if value1.lower()=="julio":
										value1=7
									else:
										if value1.lower()=="agosto":
											value1=8
										else:
											if value1.lower()=="septiembre":
												value1=9
											else:
												if value1.lower()=="octubre":
													value1=10
												else:
													if value1.lower()=="noviembre":
														value1=11
													else:
														if value1.lower()=="diciembre":
															value1=12							



			if value1 and value2 and value0:

				datos = Asistencia.objects.all().order_by("fecha_registro")

				i = 0
				color=[]
				mes=[0]*5
				mes1=[0]*5

				nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]

				for z in range(5):
					r = lambda: random.randint(0,255)
					r = lambda: random.randint(0,255)
					color.append('#%02X%02X%02X' % (r(),r(),r()))
					i+=1

				

				value0=int(value0) #Semana
				value1=int(value1) #Mes
				value2=int(value2) #Anio

				if int(value1) == 1:
					value3=12
					value5=value2-1
				else:
					value3=int(value1)-1	
					value5=value2
				
				cont=0
				cont2=0
				dia_anterior="0"
				for item in datos:

					if item.fecha_registro.year == int(value2) and item.fecha_registro.month == int(value1):
						
						#if cont==1 and item.dia=="Miercoles":
						#	cont=2

						if dia_anterior ==  item.dia:
							cont+=1
							cont2+=1


						if value0 == 1 and item.dia.lower() == "miercoles" and cont==0 and cont2==0:

							for item1 in datos:
								if item1.fecha_registro.year == int(value5) and item1.fecha_registro.month == int(value3):
									mes1[0] = item1.asistencia_hombres 
									mes1[1] = item1.asistencia_mujeres 
									mes1[2] = item1.asistencia_adolecentes 
									mes1[3] = item1.asistencia_jovenes 
									mes1[4] = item1.asistencia_niños  

							mes[0] = mes[0] + mes1[0] 
							mes[1] = mes[1] + mes1[1]
							mes[2] = mes[2] + mes1[2] 
							mes[3] = mes[3] + mes1[3] 
							mes[4] = mes[4] + mes1[4]

							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños  
							cont=2	
							cont2=2	
							break

						if value0-1 == cont//2 :		
							cont2+=1
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños
							cont=cont-1
							if cont2==2:
								break
						cont+=1		

						dia_anterior=item.dia

					#color = simplejson.dumps(color)
					#nombre=simplejson.dumps(nombre)
					#mes=simplejson.dumps(mes)	
				if value1==12:
					value3=1
					value4=value2+1
				else:
					value3=value1+1
					value4=value2	


				

				if cont2==1:
					for item in datos:
						if item.fecha_registro.year == int(value4) and item.fecha_registro.month == int(value3):
							mes[0] = mes[0] + item.asistencia_hombres 
							mes[1] = mes[1] + item.asistencia_mujeres 
							mes[2] = mes[2] + item.asistencia_adolecentes 
							mes[3] = mes[3] + item.asistencia_jovenes 
							mes[4] = mes[4] + item.asistencia_niños

							break
					


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
			mes=[0]*5
			info=" "
			nombre=["Hombres","Mujeres","Adolecentes","Jovenes","Niños"]

			i = 0
			template = loader.get_template('asistencia/grafica_semana_tipo.html')
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


def Creacion_Asistencia_Exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/creacion_asistencia_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def Edicion_Asistencia_Exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/editar_asistencia_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 	

def Eliminacion_Asistencia_Exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/eliminacion_asistencia_exitosa.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 

def AsistenciaList(request):
	if request.user.is_superuser:
		template = 'asistencia/asistencia_semanal.html'
		asistencia = Asistencia.objects.all().order_by('-fecha_registro')

		pages = pagination(request, asistencia, num=5)

		context = {
        	'items': pages[0],
        	'page_range': pages[1],
    	}
		return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')

def asistencia_search(request):
	if request.user.is_superuser:
		template = 'asistencia/asistencia_semanal.html'

		query = request.GET.get('q')
		if query:
			asistencia = Asistencia.objects.filter(Q(fecha_registro__icontains=query)|
					Q(dia__icontains=query)
				).order_by('-fecha_registro')
		else:
			asistencia = Asistencia.objects.all()

		if not asistencia.exists():
			query = elimina_tildes(query)
			asistencia = Asistencia.objects.filter(Q(fecha_registro__icontains=query)|
					Q(dia__icontains=query)
				).order_by('-fecha_registro')
			
			pages = pagination(request, asistencia, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}			
			return render(request, template, context)
		else:
			pages = pagination(request, asistencia, num=5)
			context = {
				'items': pages[0],
       			'page_range': pages[1],
       			'query': query,
			}		
			return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')
	
class AsistenciaCreate(views.SuperuserRequiredMixin,CreateView):
	model = Asistencia
	template_name = 'asistencia/asistencia_semanal_form.html'
	form_class = AsistenciaForm
	success_url = reverse_lazy('asistencia:creacion_exitosa')
	 	

class AsistenciaDelete(views.SuperuserRequiredMixin,DeleteView):
	model = Asistencia
	template_name = 'asistencia/asistencia_delete.html'
	success_url = reverse_lazy('asistencia:eliminacion_exitosa')

class AsistenciaUpdate(views.SuperuserRequiredMixin,UpdateView):
	model = Asistencia
	form_class = AsistenciaForm
	template_name = 'asistencia/asistencia_edit.html'
	success_url = reverse_lazy('asistencia:edicion_exitosa')
			