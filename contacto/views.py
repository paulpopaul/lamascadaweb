from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


from django.contrib import messages

from .forms import ContactoForm

# Create your models here.

def contacto(request):
    form = ContactoForm()
    if request.method == 'POST':
        form = ContactoForm(request.POST or NONE)
        if form.is_valid():
            form.save()
            form = ContactoForm()
            messages.success(request, "Tu mensaje ha sido recibido")
            return redirect('/contacto') 

    context = {'form':form}
    return render(request,'contact.html',context)  

'''



def contacto(request):
    form = ContactoForm()
    if request.method == 'POST':
        form = ContactoForm(request.POST or NONE)
        if form.is_valid():
            form.save()
            form = ContactoForm()
    context = {'form':form}
    return render(request,'contact.html',context)  

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido'] 
        email = request.POST['email']
        asunto = request.POST['asunto'] 
        mensaje = request.POST['mensaje']  

        contact = Contacto(nombre=nombre ,apellido=apellido ,email=email ,asunto=asunto ,mensaje=mensaje)   
        contact.save()
        messages.success(request, ": " + "Thanks for Contacting Will Seen Soon") 
        return redirect('contact')

def contacto(request):
    if request.method == "POST":
        contact = ContactoForm(request.POST or None)
        redirect_to = '/enviando/'

        if contact.is_valid():
            instance = contact.save(commit=False)
            instance.save()
            to_mail = [instance.email]
            subject = "Solicitud de Contacto"
            from_email = settings.EMAIL_HOST_USER
            context = {
                'nombre': instance.nombre,
                'apellido': instance.apellido,
                'celular': instance.celular,
                'email': instance.email,
                'mensaje': instance.mensaje
            }
            with open(settings.BASE_DIR + "/templates/contactoapp/contacto_template_detail.txt") as f:
                signup_message = f.read()
            html_template = get_template("contactoapp/contacto_template_detail.html").render(context)
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_mail)
            message.attach_alternative(html_template, "text/html")
            message.send()

            subject = "Solicitud de Contacto"
            from_email = settings.EMAIL_HOST_USER
            to_mail = ['ainsworth.developed@gmail.com']
            with open(settings.BASE_DIR + "/templates/contactoapp/contacto_template_detail.txt") as f:
                signup_message = f.read()
            html_template = get_template("contactoapp/contacto_template_detail.html").render(context)
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_mail)
            message.attach_alternative(html_template, "text/html")
            message.send()

            return redirect(redirect_to)
    else:
        contact = ContactoForm()

    context = {
        'contact': contact,
    }
    template = "contactoapp/contacto_template.html"
    return render(request, template, context)

'''