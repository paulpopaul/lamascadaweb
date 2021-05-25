from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from. models import Item, OrderItem, Order, Payment, Coupon, Used_coupon, Refund, UserProfile, Category, Slide, Order_buy, Perfil, Token_tbk, Favorite
# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Actualizar orden a reembolso concedido'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
    'ordered_date',
                    'user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',


                    'payment',
                    'coupon'
    ]
    list_display_links = [
        'user',

        'payment',
        'coupon'
    ]
    list_filter = [ 'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted'
    ]
    search_fields = [
        'id'
        'user__username',
        'ref_cod'
    ]
    actions = [make_refund_accepted]
    readonly_fields = ('id','ordered_date','items','get_total_final','coupon','get_discount_order_total','get_total')


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copiar Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'discount_price',
        'is_active',
        'category',
        'slug'
    ]
    list_filter = ['title', 'price','is_active','discount_price','category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}

    '''
    actions = [copy_items]
    '''
    fieldsets = (
        (_('Principal'), {
            'fields': ('is_active','title','description', 'slug')}),

        (_('Precio'), {
            'fields': ('price',)}),

        (_('Descuento'), {
            'fields': ('discount_price_is_active', 'discount_price')}),

        (_('Categoria'), {
            'fields': ('category',)}),

        (_('Imágenes'), {
            'fields': ('image','image2','image3', 'image4')}),

        (_('Etiqueta'), {
            'fields': ('label_is_active','label')}),

        (_('Disponibilidad'), {
            'fields': ('stock_active','stock_no')}),

        (_('Puntuación'), {
            'fields': ('stars_reputation',),
            'classes': ('collapse', 'collapse-closed')}),)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'orden',
        'is_active',
        'in_home',
    ]
    list_filter = ['title', 'is_active','in_home']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}
    

admin.site.register(Item,ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Used_coupon)

admin.site.register(Refund)
admin.site.register(UserProfile)

admin.site.register(Order_buy)
admin.site.register(Perfil)
admin.site.register(Token_tbk)

admin.site.register(Favorite)
