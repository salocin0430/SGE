from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.decorators import login_required

from apps.usuario.views import index_vistas, UsuarioCreate, UsuarioDelete, UsuarioUpdate
from apps.usuario.views import Conyuge_hijosList, Conyuge_hijosCreate, Conyuge_hijosDelete, Conyuge_hijosUpdate
from apps.usuario.views import creacion_usuario_exitosa, creacion_conyuge_hijos_exitosa, Gestion_Grupos
from apps.usuario.views import editar_conyuge_hijos_exitosa, editar_usuario_exitosa, perfil, Gestion_Miembros
from apps.usuario.views import eliminar_conyuge_hijos_exitosa, eliminar_usuario_exitosa

from .views import info_usuario, MiembroList, Conyuge_hijosListEdit
from .views import search, pariente_search, pariente_edit_search

from apps.usuario.models import Usuario, Conyuge_hijos

app_name='centro'
urlpatterns = [
    path('inicio', login_required(index_vistas), name='index_vistas'),
    url(r'^Gestion_Miembros', login_required(Gestion_Miembros), name='Gestion_Miembros'),
    url(r'^Gestion_Grupos', login_required(Gestion_Grupos), name='Gestion_Grupos'),
    url(r'^listar', login_required(MiembroList), name='usuario_listar'), #..<--
    url(r'^results', login_required(search), name='search'), #..<--
    url(r'^parientes_results', login_required(pariente_search), name='pariente_search'), #..<--
    url(r'^parien_edit_results', login_required(pariente_edit_search), name='pariente_edit_search'), #..<--
    url(r'^crear', login_required(UsuarioCreate.as_view()), name='usuario_crear'),
    url(r'^eliminar/(?P<pk>\d+)/$', login_required(UsuarioDelete.as_view()), name='usuario_eliminar'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(UsuarioUpdate.as_view()), name='usuario_editar'),
    url(r'^conyuge_hijos_listar', login_required(Conyuge_hijosList), name='conyuge_hijos_listar'),
    url(r'^register_conyuge_hijos_listar', login_required(Conyuge_hijosListEdit), name='Conyuge_hijosListEdit'),
    url(r'^conyuge_hijos_crear/(\w+)/$', login_required(Conyuge_hijosCreate), name='conyuge_hijos_crear'),
    url(r'^conyuge_hijos_eliminar/(?P<pk>\d+)/$', login_required(Conyuge_hijosDelete.as_view()), name='conyuge_hijos_delete'),
    url(r'^conyuge_hijos_editar/(?P<pk>\d+)/$', login_required(Conyuge_hijosUpdate.as_view()), name='conyuge_hijos_editar'),
    url(r'^creado_correctamente', login_required(creacion_conyuge_hijos_exitosa), name='creacion_exitosa'),
    url(r'^creado_usuario_correctamente', login_required(creacion_usuario_exitosa), name='creacion_usuario_exitosa'),
    url(r'^editado_conyuge_hijos_correctamente', login_required(editar_conyuge_hijos_exitosa), name='edicion_exitosa'),
    url(r'^editado_usuario_correctamente', login_required(editar_usuario_exitosa), name='edicion_usuario_exitosa'),
    url(r'^eliminado_conyuge_hijos_correctamente', login_required(eliminar_conyuge_hijos_exitosa), name='eliminado_pariente_exitosa'),
    url(r'^eliminado_usuario_correctamente', login_required(eliminar_usuario_exitosa), name='eliminado_usuario_exitosa'),
    url(r'^perfil_del_usuario/(\w+)/$', login_required(perfil.as_view()), name='perfil_usuario'),
    url(r'^exportar/(?P<pk>[0-9]+)/$', login_required(info_usuario), name='exportar_pdf'),
]
