from django.urls import path
from . import views


urlpatterns = [
    path('',views.allorders, name='allorders'),
    path('detail/<str:buy_order>/',views.orderdetail, name='orderdetail'),

]