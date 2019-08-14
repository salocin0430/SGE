"""iglesia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout_then_login, password_reset, password_reset_done
from django.contrib.auth.views import password_reset_confirm, password_reset_complete, login

from apps.usuario.views import pantallaInicio,mision


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', pantallaInicio, name='pantallaInicio'),
    path('mision', mision, name='mision'),
    url(r'^Registro_Membresia/', include('apps.usuario.urls')),
    path('usuario/', include ('apps.usuario.urls', namespace="usuario")),
    path('login/', include ('apps.login.urls', namespace="login")),
    path('asistencia/', include ('apps.asistencia.urls', namespace="asistencia")),
    path('grupos/', include ('apps.grupos.urls', namespace="grupos")),
    url(r'^accounts/login/',login, {'template_name':'index.html'}, name='loginsession'),
    url(r'^logout/',logout_then_login,name='logout'),
    url(r'^reset/password_reset', password_reset, 
        {'template_name':'registration/password_reset_form.html',
        'email_template_name': 'registration/password_reset_email.html'}, 
        name='password_reset'), 
    url(r'^password_reset_done', password_reset_done, 
        {'template_name': 'registration/password_reset_done.html'}, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, 
        {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
    #url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)