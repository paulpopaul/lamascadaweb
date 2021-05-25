from django.shortcuts import render ,redirect ,get_list_or_404
from core.models import Perfil, Order, OrderItem, Order_buy 
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@staff_member_required()
def allorders(request):
    order = Order_buy.objects.order_by('-order_id')

    for product in order:
        userid = product.user_id

    perfil_info = Perfil.objects.filter(user=userid)

    context = {
        'order' :order ,
        'perfil_info' : perfil_info ,
    }

    return render(request,'adminorders/adminorders.html',context)


@staff_member_required()
def orderdetail(request, buy_order):
    order = Order.objects.get( buy_order=buy_order)
    orders = get_list_or_404(Order, buy_order=buy_order)
    orderbuy = Order_buy.objects.get(buy_order=buy_order)
    orderitem = OrderItem.objects.filter(buy_order=buy_order)

    for product in orders:
        userid = product.user_id

    perfil_info = Perfil.objects.filter(user=userid).last()

    context = {
        'order' : order,
        'orders' : orders ,
        'orderbuy': orderbuy,
        'orderitem':orderitem,
        'buy_order' : buy_order ,
        'perfil_info' : perfil_info ,
    }

    return render(request,'adminorders/orderdetail.html',context)


