from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ItemDetailView,
    ItemListView,
    HomeView, 
    ShopView,
    OrderSummaryView, 
    CheckoutView,
    add_to_cart, 
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    CategoryView,
    Preciominmax,
    dashboard,
    details,
    profiles,
    thankyou,
    favorite_inf,
    addtofavorite,
    removefavorite,
)

from . import views

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('order_summary', OrderSummaryView.as_view(), name='order_summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product_related/', ItemListView.as_view(), name='produc_related'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('tienda/', ShopView.as_view(), name='shop'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request_refund/', RequestRefundView.as_view(), name='request_refund'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profiles, name='profiles'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('order_ok/', TemplateView.as_view(template_name="order_buy/order_ok.html"), name='order_ok'),
    path('order_error/', TemplateView.as_view(template_name="order_buy/order_error.html"), name='order_error'),
    path('details/<str:buy_order>/', views.details, name='details'),
    path('addtofavorite',views.addtofavorite,name='addtofavorite'),
    path('removefavorite',views.removefavorite,name='removefavorite'),
    path('favorites',views.favorite_inf,name='favorites'),
]
