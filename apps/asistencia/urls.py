from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.asistencia.views import AsistenciaCreate, AsistenciaList, AsistenciaDelete, AsistenciaUpdate
from apps.asistencia.views import Creacion_Asistencia_Exitosa, Edicion_Asistencia_Exitosa, graficaSemana,graficaAnio, graficaMes,TiposgraficaAnio,TiposgraficaMes,TiposgraficaSemana
from apps.asistencia.views import Eliminacion_Asistencia_Exitosa, asistencia_search

app_name = 'centro'
urlpatterns = [
	url(r'^asistenciacrear', login_required(AsistenciaCreate.as_view()), name='crear'),
	
	url(r'^graficaAnio', login_required(graficaAnio), name='graficaAnio'),
	url(r'^graficaMes', login_required(graficaMes), name='graficaMes'),
	url(r'^graficaSemana', login_required(graficaSemana), name='graficaSemana'),

	url(r'^TiposgraficaAnio', login_required(TiposgraficaAnio), name='TiposgraficaAnio'),
	url(r'^TiposgraficaMes', login_required(TiposgraficaMes), name='TiposgraficaMes'),
	url(r'^TiposgraficaSemana', login_required(TiposgraficaSemana), name='TiposgraficaSemana'),
	
	url(r'^asistencialistar', login_required(AsistenciaList), name='listar'),
	url(r'^result', login_required(asistencia_search), name='asistencia_search'),
	url(r'^asistenciaeditar/(?P<pk>\d+)/$', login_required(AsistenciaUpdate.as_view()), name='asistencia_editar'),
	url(r'^asistenciaeliminar/(?P<pk>\d+)/$', login_required(AsistenciaDelete.as_view()), name='asistencia_eliminar'),
	url(r'^asistencia_creacion_exitosa', login_required(Creacion_Asistencia_Exitosa), name='creacion_exitosa'),
	url(r'^asistencia_edicion_exitosa', login_required(Edicion_Asistencia_Exitosa), name='edicion_exitosa'),
	url(r'^asistencia_eliminacion_exitosa', login_required(Eliminacion_Asistencia_Exitosa), name='eliminacion_exitosa'),
]