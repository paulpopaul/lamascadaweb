from django.urls import path
from .views import ImagenView

# Create your views here.

urlpatterns = [
    path('', ImagenView.as_view(), name='carta'),
]