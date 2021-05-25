from django.conf import settings

# Mailing
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage

# Vistas
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET, require_POST

# Transbank
#from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
import os
from django.utils import timezone
from datetime import datetime
import random
import tbk

# Proyecto
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, PerfilForm, UserProfileForm, TokenForm
from .models import Item, OrderItem, Order, Payment, Coupon, Used_coupon, Refund, UserProfile, Category, Order_buy, Perfil, Token_tbk, Favorite
from .filters import ItemFilter
from django.db.models import Count

# Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


#Stripe
#import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    
def is_valid_form(values):
    valid = True
    for field in values:
        if field =='':
            valid = False
    return valid



def Preciominmax(request):
    if request.method == "POST":
        preciominimo = request.POST.get('preciominimo')
        preciomaximo = request.POST.get('preciomaximo')
        resultado = Item.objects.raw('select id_item, title, price from core_item where price between "'+preciominimo+'" and "'+preciomaximo+'" ')
        return render(request, 'shop.html', {'data':resultado})

    else: 
        itemss = Item.objects.all()
        return render(request, 'preciominmax.html', {'data':itemss})

 

class HomeView(ListView):
    template_name = "home.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'
    
    def get(self, *args, **kwargs):
        category = Category.objects.filter(is_active=True, in_home=True).order_by('orden')[:9]
        item = Item.objects.filter( is_active=True)
        context = {
            'object_list': item,
            'category_list': category,
        }
        return render(self.request, "home.html", context)



class ShopView(ListView):
    model = Item
    queryset = Item.objects.filter(is_active=True)
    template_name = "shop.html"
    paginate_by = 15
    filterset_class = ItemFilter
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        object_list = self.get_queryset() 
        user_filter = ItemFilter(self.request.GET, queryset=object_list) 
        context = super().get_context_data(object_list=user_filter.qs, user_filter=user_filter, **kwargs)
        context['filter'] = ItemFilter(self.request.GET, queryset=self.get_queryset())
        context['result'] = self.get_queryset().count()
        context['all_items'] = str(Item.objects.filter(is_active=True).count())
        context["itemcount"] = self.request.GET.get('paginate_by', self.paginate_by)
        return context



class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        context['object_list'] = Item.objects.all()[:8]
        context['orderitem'] = OrderItem.objects.filter()
        context['object_list_slug'] = Category.objects.all()
        context['order'] = Order.objects.filter()
        return context



class ItemListView(ListView):
    model = Item
    template_name = "product_related.html"



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            item = Item.objects.filter( is_active=True)
            context = {
                'object': order,
                'item': item,
                'couponform': CouponForm(),
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'No tienes un pedido activo.')
            return redirect("/")



class CategoryView(ListView):
    model = Item
    category = Category.objects.all()
    queryset = Item.objects.filter(category=category, is_active=True)
    template_name = "category.html"
    paginate_by = 12
    filterset_class = ItemFilter
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        object_list = Item.objects.filter(category=category, is_active=True)
        user_filter = ItemFilter(self.request.GET, queryset=object_list) 
        context = super().get_context_data(object_list=user_filter.qs, user_filter=user_filter, **kwargs)
        context['filter'] = ItemFilter(self.request.GET, queryset=self.get_queryset())
        context['all_items'] = str(Item.objects.filter(category=category, is_active=True).count())
        context["itemcount"] = self.request.GET.get('paginate_by', self.paginate_by)
        context["category_title"] = category = Category.objects.get(slug=self.kwargs['slug'])
        return context


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            order_item = OrderItem.objects.filter(user=self.request.user, ordered=False)
            perfil_account = Perfil.objects.filter(user=self.request.user).last()
            profile = PerfilForm()
            context = {
                'profile': PerfilForm(),
                'couponform': CouponForm(),
                'order': order,
                'order_item':order_item,
                'DISPLAY_COUPON_FORM': True,
                'perfil_account' : perfil_account,

            }
            return render(self.request, "checkout.html", context) 
        except ObjectDoesNotExist:
            messages.info(self.request, "No tiene una orden activa.")
            return redirect('/')

    def post(self, *args, **kwargs):
        profile = PerfilForm(self.request.POST or None)
        if profile.is_valid():
            profile = profile.save(commit=False)
            profile.user = self.request.user
            profile.save()
            profile = PerfilForm()
            return redirect('/integracion_tbk/normal_index/') 
        messages.warning(self.request, "Formulario incompleto")
        return redirect('core:checkout') 
        context = {
            'profile':profile,    
            }
        return render(self.request,'checkout.html',context) 
         
    def init(request):
        template_name = 'integracion_tbk/base.html'
        return render(request,template_name)



class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "No tienes una dirección de PAGO.")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()


                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.buy_order = create_ref_code()
                order.save()

                '''
                msg = "Usuario:{} Descuento:{} Total:{} Code:{}".format(order.user, order.get_discount_order_total(), order.get_total(), order.ref_code)

                email = EmailMessage('Hello',
                    msg,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.request.user.email],
                )
                email.send(fail_silently=True)
                '''

                messages.success(self.request, "Su orden fue exitosa!.")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")
    

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request,"Ítem: " + item.title + " fue actualizado (+1)")
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.success(request, "Ítem: " + item.title + " fue agregado a su carrito")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request,"Ítem: " + item.title + " fue actualizado (+1)")
        return redirect("core:order_summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request,"Ítem: " + item.title + " fue eliminado (x)")
            return redirect("core:order_summary")
        else:
            messages.info(request, "Este artículo no estaba en tu carrito.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "No tienes un pedido activo.")
        return redirect("core:product", slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,"Ítem: " + item.title + " fue actualizado (-1)")
            return redirect('core:order_summary')
        else:
            messages.info(request, "Este artículo no estaba en tu carrito.")
            return redirect('core:product', slug=slug)
    else:
        messages.info(request, "No tienes un pedido activo.")
        return redirect('core:product', slug=slug)

'''
@login_required(login_url='login')
def get_coupon(request, code):
    now = timezone.now()
    coupon = Coupon.objects.get(code=code, 
            valid_from__lte=now,
            valid_to__gte=now,
            coupon_active=True)
    add_used = Used_coupon(user=request.user,code=code)
    add_used.save()
    return coupon
'''


@login_required
def get_coupon(request, code):
    now = timezone.now()
    coupon = Coupon.objects.get(code=code, 
            valid_from__lte=now,
            valid_to__gte=now,
            coupon_active=True)
    add_used = Used_coupon(user=request.user,code=code)
    add_used.save()
    return coupon

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                coupon = Coupon.objects.get(code=code)
                if Coupon.objects.all().filter(code=code).exists():
                    coupon = Coupon.objects.get(code=code)
                    if coupon.coupon_active :
                        if Used_coupon.objects.all().filter(user=self.request.user,code=code).exists():
                            messages.info(self.request,"Error: El cupón "+ coupon.code +" ya ha sido utilizado")
                            return redirect('core:checkout')
                        else:
                            order.coupon = get_coupon(self.request, code)
                            order.save()
                            messages.success(self.request, 'Su cupón ' +coupon.code +' ha sido aplicado exitosamente!')
                            return redirect('core:checkout')
                    else:
                        messages.error(self.request,"Error: El cupón "+ coupon.code +" expiró ")
                        return redirect('core:checkout')
                else:
                    messages.error(self.request," Este cupón no existe ")
                    return redirect('core:checkout')
                    
            except ObjectDoesNotExist:
                messages.info(self.request, 'Este cupón no existe')
                return redirect('core:checkout')  


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            buy_order = form.cleaned_data.get('buy_order')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(buy_order=buy_order)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Tu solicitud ha sido recibida")
                return redirect('core:request_refund')

            except ObjectDoesNotExist:
                messages.info(self.request, "Esta orden no existe.")
                return redirect('core:request_refund')



@login_required
def dashboard(request):
    user_orders = Order.objects.all().filter(user=request.user).order_by('-start_date')

    userprofile = UserProfile.objects.get(user=request.user)
    order_buy = Order_buy.objects.filter()

    context = {
        'orders' : user_orders,
        'userprofile' : userprofile,
        'order_buy': order_buy,

    }
    return render(request,'accounts/dashboard.html',context)    


@login_required
def details(request,buy_order):
    orders = get_list_or_404(Order, user=request.user, buy_order=buy_order)
    order = Order.objects.all().filter(user=request.user)
    payments = get_list_or_404(Payment, user=request.user)
    payment = Order.objects.all().filter(user=request.user)
    items = get_list_or_404(Item)
    item = Item.objects.all()
    order_items = get_list_or_404(OrderItem,user=request.user)
    order_item = OrderItem.objects.filter(user=request.user, buy_order=buy_order)
    order_buy = Order_buy.objects.filter(user=request.user, buy_order=buy_order)
    context = {
        'orders' : orders ,
        'buy_order' : buy_order ,
        'payment': payment,
        'payment':payment,
        'items':items,
        'item':item,
        'order_item': order_item,
        'order_items': order_items,
        'order_buy': order_buy,
    }
    return render(request,'accounts/bought.html',context)


@login_required
def profiles(request):
    try:
        perfil_account = Perfil.objects.filter(user=request.user).last()
        order_buy = Order_buy.objects.filter(user=request.user).count
        order_item = OrderItem.objects.filter(user=request.user, ordered=True).count
        coupon_used = Used_coupon.objects.filter(user=request.user).count
        favorites = Favorite.objects.all().filter(user_id=request.user.id).count

        context = {
            'perfil_account' : perfil_account,
            'order_buy': order_buy,
            'order_item': order_item,
            'coupon_used':coupon_used,
            'favorites':favorites,

        }
        return render(request,'accounts/profile.html',context)    
    except ObjectDoesNotExist:
        messages.warning(request, 'no tienes un pedido activo.')
        return redirect("accounts/profile.html")


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.template import Context

@login_required
def thankyou(request):
    try:
        perfil_account = Perfil.objects.all().last()
        order = Order.objects.get(user=request.user, ordered=False)
        orderitem = OrderItem.objects.filter(user=request.user, ordered=False)
        orderbuy = Order_buy.objects.all()

        orderbuy = Order_buy()
        orderbuy.user = request.user
        orderbuy.buy_order = create_ref_code()
        orderbuy.save()

        plaintext = get_template('send_email_voucher/email_voucher_detail.txt')
        htmly = get_template('send_email_voucher/email_voucher_detail.html')

        context = {
            'username': request.user.username,
            'perfil_account' : perfil_account,
            'order': order,
            'orderitem':orderitem,
            'orderbuy':orderbuy,
        }

        to_mail = request.user.email
        subject, from_email, to = ''+perfil_account.first_name+', gracias por tu compra en La Mascada!', 'contacto@lamascada.cl', to_mail,

        text_content = plaintext.render(context)
        html_template = htmly.render(context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_template, "text/html")
        msg.send()

        amount = int(order.get_total() * 100)
        # create the payment

        payment = Payment()
        payment.user = request.user
        payment.amount = order.get_total()
        payment.stripe_charge_id = orderbuy.buy_order
        payment.save()

        order_items = order.items.all()
        order_items.update(ordered=True)
        order_items.update(buy_order=orderbuy.buy_order)

        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.user = request.user
        order.buy_order = orderbuy.buy_order
        order.save()
        orders = Order.objects.filter(user=request.user, ordered=True).last()

        context = {
            'orders':orders,
        }

        return render(request, 'thankyou.html', context)

    except ObjectDoesNotExist:
        return redirect("/")

def token_tbk(request):
    form = TokenForm()
    if request.method == 'POST':
        form = TokenForm(request.POST or NONE)
        if form.is_valid():
            form.save()
            form = TokenForm()
            messages.success(request, "Tu solicitud ha sido recibida")
            return redirect('/contacto') 

    context = {'form':form}
    return render(request,'integracion_tbk/final_normal.html',context)  




@login_required
def addtofavorite(request):
    if request.method == 'POST':
        user_id = request.user.id
        product_id = request.POST['product_id']
        product_slug = request.POST['product_slug']
        product_name = request.POST['product_name']
        product_photo = request.POST['product_photo']
        product_price = request.POST['product_price']
        if Favorite.objects.all().filter(user_id=user_id ,product_id=product_id).exists():
            messages.warning(request ,"Ítem: " + product_name + " ha sido agregado antes")
            return redirect('/favorites')
        else :    
            favorite = Favorite(user_id=user_id , product_id=product_id, product_slug=product_slug, product_name=product_name , product_photo=product_photo , product_price=product_price)
            favorite.save()
            messages.success(request ,"Ítem: " + product_name + " ha sido agregado a favoritos")
            return redirect('/favorites')




@login_required
def favorite_inf(request):
    favorites = Favorite.objects.all().filter(user_id=request.user.id)
    context = {
        'favorites':favorites,
    }      
    return render(request,'accounts/favorite.html',context)  




@login_required
def removefavorite(request):
    if request.method == 'POST' :
        user_id = request.user.id
        product_id = request.POST['product_id']
        product_slug = request.POST['product_slug']
        product_name = request.POST['product_name']
        favorites_id = request.POST['favorites_id']
        fav = Favorite.objects.all().filter(id=favorites_id, product_slug=product_slug, product_name=product_name,product_id=product_id)
        fav.delete()
        messages.info(request,"Ítem: " + product_name + " ha sido eliminado de favoritos" )
        return redirect('/favorites')




