"""lamascadaweb URL Configuration

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

        'path('contact/', include(('contacto.urls', 'contacto'), namespace='contacto')),'

"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('nosotros/', include(('galeriaapp.urls', 'imagen'), namespace='imagen')),
    path('contacto/', include(('contacto.urls', 'contacto'), namespace='contacto')),
    path('integracion_tbk/',include('integracion_tbk.urls')) ,
    path('profile/', TemplateView.as_view(template_name="accounts/profile.html"), name='profile'),
    path('carta/', include(('cartaapp.urls', 'carta'), namespace='carta')),

    path('adminorders/', include('adminorders.urls')),
    path('suscripcion/', include(('suscripcion.urls', 'suscripcion'), namespace='suscripcion')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)