from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import Imagen

# Create your views here.


class ImagenView(ListView):
    template_name = "about.html"
    queryset = Imagen.objects.all()
    context_object_name = 'items'

