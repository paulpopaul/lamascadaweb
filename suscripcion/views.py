from django.shortcuts import render,redirect
from django.conf import settings


from django.contrib import messages
from .forms import SuscripcionUsuarioForm


def suscripcion(request):
    suscripcionform = SuscripcionUsuarioForm()
    if request.method == 'POST':
        suscripcionform = SuscripcionUsuarioForm(request.POST or NONE)
        if suscripcionform.is_valid():
            suscripcionform.save()
            suscripcionform = SuscripcionUsuarioForm()
            messages.success(request, "Suscripción realizada con éxito")
            return redirect('/') 

    context = {'suscripcionform':suscripcionform}
    return render(request,'suscripcion/suscripcion_usuario.html',context)  