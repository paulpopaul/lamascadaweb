from django.urls import path
from .views import suscripcion

# Create your views here.

urlpatterns = [
    path('', suscripcion, name='suscripcion'),
]