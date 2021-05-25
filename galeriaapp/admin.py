from django.contrib import admin
from .models import Imagen

# Register your models here.

class ImagenAdmin(admin.ModelAdmin):
    list_display = ('numero_id','estado','creado')
    list_filter = ('estado', 'creado')

admin.site.register(Imagen, ImagenAdmin)