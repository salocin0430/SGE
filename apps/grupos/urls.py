from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.decorators import login_required

from apps.grupos.views import GruposList, GruposCreate, GruposDelete, GruposUpdate, editar_grupos_exitosa
from apps.grupos.views import eliminacion_grupos_exitosa, creacion_grupos_exitosa
from apps.grupos.views import grupo_search, Info, pdf_grupos_view
from apps.grupos.views import graficaAnio,graficaMes

app_name='centro'
urlpatterns = [
	url(r'^listar', login_required(GruposList), name='grupos_listar'),
	url(r'^result', login_required(grupo_search), name='grupo_search'),
	url(r'^crear', login_required(GruposCreate.as_view()), name='grupos_crear'),
	url(r'^editar/(?P<pk>\d+)/$', login_required(GruposUpdate.as_view()), name='grupos_editar'),
	url(r'^eliminar/(?P<pk>\d+)/$', login_required(GruposDelete.as_view()), name='grupos_eliminar'),
	url(r'^creacion_exitosa', login_required(creacion_grupos_exitosa), name='creacion_exitosa'),
	url(r'^edicion_exitosa', login_required(editar_grupos_exitosa), name='edicion_exitosa'),
	url(r'^eliminacion_exitosa', login_required(eliminacion_grupos_exitosa), name='eliminacion_exitosa'),
	url(r'^info_grupo/(\w+)/$', login_required(Info.as_view()), name='informacion_grupo'),
	url(r'^exportar/(?P<pk>[0-9]+)/$', login_required(pdf_grupos_view), name='exportar_pdf'),
	url(r'^graficaAnio', login_required(graficaAnio), name='graficaAnio'),
	url(r'^graficaMes', login_required(graficaMes), name='graficaMes'),
]	