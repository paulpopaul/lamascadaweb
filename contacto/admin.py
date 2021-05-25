from django.contrib import admin

# Register your models here.

from .models import Contacto

class ContactoAdmin(admin.ModelAdmin):
    model = Contacto
    fieldsets = (
        (('Mensaje'), {
            # 'classes': ('collapse',),
            'fields': (('nombre',),( 'apellido',),('email',) ,('asunto'),
                       ('mensaje',),
                       ), }),
    )
    list_display = ['nombre', 'apellido', 'fecha']
    search_fields = ('nombre', 'apellido', 'email','celular' , 'mensaje')
    list_filter = ['nombre', 'apellido', 'fecha', ]

admin.site.register(Contacto, ContactoAdmin)

