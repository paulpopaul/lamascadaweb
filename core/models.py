from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.



LABEL_CHOICES = (
    ('Nuevo','nuevo'),
    ('Promoción','promocion'),
)


STARS_CHOICES = (
    ('1','una'),
    ('2','dos'),
    ('3','tres'),
    ('4','cuatro'),
    ('5','cinco'),
)


ADDRESS_CHOICES = (
    ('B','Pago'),
    ('S','Envío')
)



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    phone = models.CharField(max_length=200)
    order_notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Perfil de usuarios'



class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)



class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)
    in_home = models.BooleanField(default=False)
    orden = models.CharField(max_length=10,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    class Meta:
        verbose_name_plural = 'Categorias'



class Item(models.Model):
    id_item = models.AutoField(primary_key=True, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField()
    price = models.IntegerField()
    discount_price_is_active = models.BooleanField(default=False)
    discount_price = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],blank=True, null=True, default='0')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)
    label_is_active = models.BooleanField(default=False)
    label = models.CharField(choices=LABEL_CHOICES,max_length=100, default='Nuevo')
    stock_active = models.BooleanField(default=True)
    stock_no = models.CharField(max_length=10,blank=True, null=True)
    stars_reputation = models.CharField(choices=STARS_CHOICES, max_length=20, default='4')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug': self.slug
        })
    def get_discount_item_ahorro(self):
        return self.price * self.discount_price / 100 

    def get_amount_saved_new_price(self):
        return self.price - self.get_discount_item_ahorro()

    class meta:
        db_table:"core_item"



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buy_order = models.CharField(max_length=20,blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_only_item(self):
        return  f"{self.quantity} of {self.item.slug}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item(self):
        return self.item.price * self.item.discount_price / 100 

    def get_total_discount_item_price(self):
        return self.get_discount_item() * self.quantity

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    class Meta:
        verbose_name_plural = 'Orden de items'



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buy_order = models.CharField(max_length=20,blank=True)
    items = models.ManyToManyField(OrderItem,blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_discount_order_total(self):
        total = 0
        for order_item in self.items.all():
            total -= round(order_item.get_amount_saved() * self.coupon.amount / 100)
        return total
    
    def get_total_final(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        if self.coupon:
            total -= round(self.get_total_final() * self.coupon.amount / 100)
        return total

    class Meta:
        verbose_name_plural = 'Orden'



class Order_buy(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buy_order = models.CharField(max_length=20,blank=True)
    created = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.buy_order

    class Meta:
        verbose_name_plural = 'Orden de compra'



class Perfil(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    phone = models.CharField(max_length=200)
    order_notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Recibos'



class Token_tbk(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transbank_tkn = models.CharField(max_length=200,blank=True, null=True)
    ordered = models.BooleanField(default=False)




class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_slug = models.SlugField()
    product_name = models.CharField(max_length=200)
    product_photo = models.CharField(max_length=300)
    product_price = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name



class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50,blank=True, null=True)
    transbank_tkn = models.CharField(max_length=200,blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Pagos'



class Coupon(models.Model):
    coupon_active = models.BooleanField(default=True)
    code = models.CharField(max_length=15,default=0)
    valid_from = models.DateTimeField()
    valid_to= models.DateTimeField()
    amount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Cupón'



class Used_coupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Cupón usado'



class Refund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name_plural = 'Reembolso'


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


