"""keyManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings

from django.conf.urls.static import static

from django.shortcuts import redirect

admin.site.enable_nav_sidebar = False
admin.site.site_header = "Administration"
admin.site.site_title = "Backend"
admin.site.index_title = "Datenbank-Tabellen"


urlpatterns = [
    path('', lambda r: redirect('/keys/')),
    path('accounts/', include('django.contrib.auth.urls'), name='account'),
    path('oidc/', include('mozilla_django_oidc.urls'), name='oidc'),

    path('admin/', admin.site.urls, name='admin'),

    path('api/', include('api.urls'), name='api'),
    path('keys/', include('keys.urls'), name='keys'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
