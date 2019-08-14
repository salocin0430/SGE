from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.login.views import eliminacion_user_exitosa,RegistroUsuario,eliminar_user, editaruser, user_edit_2, editaruser1, editar_usuario_exitosa
from apps.login.views import UserRegisterList, Usersearch

app_name = 'centro'
urlpatterns = [
	path('registrar', login_required(RegistroUsuario), name='registrar'),
	url(r'^userresults', login_required(Usersearch), name='usersearch'), #..<--
	#path('registrar', login_required(RegistroUsuario.as_view()), name='registrar'),
	url(r'^editar_user', login_required(editaruser), name='editar_user'),
	url(r'^user_edit_2/(?P<pk>\d+)/$', login_required(user_edit_2.as_view()), name='user_edit_2'),
	url(r'^editar', login_required(editaruser1), name='editar'),
	url(r'^eliminar/(?P<pk>\d+)/$', login_required(eliminar_user.as_view()), name='user_eliminar'),
	url(r'^editado_usuario_correctamente', login_required(editar_usuario_exitosa), name='edicion_usuario_exitosa'),
	url(r'^eliminado_user_exitoso', login_required(eliminacion_user_exitosa), name='eliminado_user_exitoso'),
	url(r'^listado_user_register', login_required(UserRegisterList), name='user_register'),
]


