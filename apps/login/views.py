from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password 
from django.http import HttpResponseForbidden, HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from apps.login.forms import RegistroForm

from django.db.models import Q

from django.views.generic import TemplateView
from mixin import Mixin, mixin
from braces import views


def UserRegisterList(request):
	if request.user.is_superuser:
		template = loader.get_template('user/user_register_list.html')

		if request.method == 'POST':
			flag = True
			template = loader.get_template('user/user_register_list.html')
			value = request.POST.get("value")
			value1 = request.POST.get("value1")

			if value and value1:
				usuario = User.objects.filter(username__exact = value)
				if usuario.exists():
					usuario = User.objects.get(username__exact = value)
					if usuario.check_password(value1):

						usuario = User.objects.filter(username__exact = value)

						ctx = {
							'usuarios' : usuario,
							'flag' : flag,
						}
						return HttpResponse(template.render(ctx,request))
						
					else:
						usuario = User.objects.filter(username__exact = value, password__exact = value1)
						ctx = {
							'usuarios' : usuario,
							'flag' : flag,
						}
						return HttpResponse(template.render(ctx,request))
				else:
					usuario = User.objects.filter(username__exact = value, password__exact = value1)
					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))			
			else:
					usuario = User.objects.filter(username__exact = value, password__exact = value1)
					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))	

		if request.method == 'GET':
			flag = False
			usuarios = User.objects.all
			template = loader.get_template('user/user_register_list.html')
			ctx = {
				'usuarios' : usuarios,
				'flag' : flag,
			}
			return HttpResponse(template.render(ctx,request))
	else:
		return render(request, 'mensajes/error_no_super_user.html') 

def Usersearch(request):
	if request.user.is_superuser:
		template = 'user/user_register_list.html'

		query = request.GET.get('q')
		if query:
			usuario = User.objects.filter(Q(username__icontains=query)|
					Q(first_name__icontains=query)|
					Q(last_name__icontains=query)
				).order_by('username')
		else:
			usuario = User.objects.all()

		if not usuario.exists():
			query = elimina_tildes(query)
			usuario = User.objects.filter(Q(username__icontains=query)|
					Q(first_name__icontains=query)|
					Q(last_name__icontains=query)
				).order_by('username')

			context = {
				'usuarios': usuario,
       			'query': query,
			}
			return render(request, template, context)
		else:
			context = {
				'usuarios':usuario,
       			'query': query,
			}
			return render(request, template, context)
	else:
		return render(request, 'mensajes/error_no_super_user.html')


def RegistroUsuario(request):
	if request.user.is_superuser: 
	    if request.method =='POST':
	    	value = request.POST.get('username')
	    	if value:
	    		userlogin = User.objects.filter(username__exact=value)
	    		if userlogin.exists():
	    			return render(request, 'mensajes/error_username_existente.html')
	    		else: 
			        form = RegistroForm(request.POST)
			        if form.is_valid():
			            form.save()
			            return render(request, 'mensajes/creacionusercorrecta.html')
			        else:
			        	return render(request, 'mensajes/creacion_error_user.html')
	    else:
	        form = RegistroForm()

	else:
		return render(request, 'mensajes/error_no_super_user.html') 

	return render(request, 'login/signup.html', {'form': form})	   

'''class RegistroUsuario(CreateView):
	model = User
	template_name = 'login/registrar.html'
	form_class = RegistroForm
	success_url = reverse_lazy('usuario:index_vistas')'''

def editar_usuario_exitosa(request):
	return render(request, 'mensajes/editar_user_exitosa.html')	

class user_edit_2(UpdateView):
	model = User
	form_class = RegistroForm
	template_name = 'user/user_edit_2.html'
	success_url = reverse_lazy('login:edicion_usuario_exitosa')
	
def editaruser(request):
	template = loader.get_template('user/user_edit_0.html')

	if request.method == 'POST':
		flag = True
		template = loader.get_template('user/user_edit_0.html')
		value = request.POST.get("value")
		value1 = request.POST.get("value1")

		if value and value1:
			usuario = User.objects.filter(username__exact = value)
			if usuario.exists():
				usuario = User.objects.get(username__exact = value)
				if usuario.check_password(value1):

					usuario = User.objects.filter(username__exact = value)

					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))
					
				else:
					usuario = User.objects.filter(username__exact = value, password__exact = value1)
					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))
			else:
				usuario = User.objects.filter(username__exact = value, password__exact = value1)
				ctx = {
					'usuarios' : usuario,
					'flag' : flag,
				}
				return HttpResponse(template.render(ctx,request))			
		else:
				usuario = User.objects.filter(username__exact = value, password__exact = value1)
				ctx = {
					'usuarios' : usuario,
					'flag' : flag,
				}
				return HttpResponse(template.render(ctx,request))		
			
					

	if request.method == 'GET':
		flag = False
		usuarios = User.objects.all
		template = loader.get_template('user/user_edit_0.html')
		ctx = {
			'usuarios' : usuarios,
			'flag' : flag,
		}
		return HttpResponse(template.render(ctx,request))


def editaruser1(request):
	template = loader.get_template('user/user_edit.html')

	if request.method == 'POST':
		flag = True
		template = loader.get_template('user/user_edit.html')
		value = request.POST.get("value")
		value1 = request.POST.get("value1")

		if value and value1:
			usuario = User.objects.filter(username__exact = value)
			if usuario.exists():
				usuario = User.objects.get(username__exact = value)
				if usuario.check_password(value1):

					usuario = User.objects.filter(username__exact = value)

					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))
					
				else:
					usuario = User.objects.filter(username__exact = value, password__exact = value1)
					ctx = {
						'usuarios' : usuario,
						'flag' : flag,
					}
					return HttpResponse(template.render(ctx,request))
			else:
				usuario = User.objects.filter(username__exact = value, password__exact = value1)
				ctx = {
					'usuarios' : usuario,
					'flag' : flag,
				}
				return HttpResponse(template.render(ctx,request))			
		else:
				usuario = User.objects.filter(username__exact = value, password__exact = value1)
				ctx = {
					'usuarios' : usuario,
					'flag' : flag,
				}
				return HttpResponse(template.render(ctx,request))	

	if request.method == 'GET':
		flag = False
		usuarios = User.objects.all
		template = loader.get_template('user/user_edit.html')
		ctx = {
			'flag' : flag,
		}
		return HttpResponse(template.render(ctx,request))

class eliminar_user(views.SuperuserRequiredMixin,DeleteView):
	model = User
	template_name = 'user/user_delete.html'
	success_url = reverse_lazy('login:eliminado_user_exitoso')	


def eliminacion_user_exitosa(request):
	if request.user.is_superuser:
		return render(request, 'mensajes/eliminacion_user.html')
	else:
		return render(request, 'mensajes/error_no_super_user.html') 
		
				