from django.shortcuts import render
from django.views.generic import ListView

from .models import Carta

# Create your views here.


class ImagenView(ListView):
    template_name = "carta.html"
    queryset = Carta.objects.all()
    context_object_name = 'carta'

