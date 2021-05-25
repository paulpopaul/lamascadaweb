from django.urls import path
from .views import contacto

# Create your views here.

urlpatterns = [
    path('', contacto, name='contacto'),

]