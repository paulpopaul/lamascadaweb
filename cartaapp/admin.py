from django.contrib import admin
from .models import Carta

# Register your models here.

class CartaAdmin(admin.ModelAdmin):
    list_display = ('numero_id','estado','creado')
    list_filter = ('estado', 'creado')

admin.site.register(Carta, CartaAdmin)


