from django.contrib import admin

# Register your models here.

from .models import SuscripcionUsuario, SuscripcionControl

admin.site.register(SuscripcionUsuario)
admin.site.register(SuscripcionControl)
