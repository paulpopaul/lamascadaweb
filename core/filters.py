
import django_filters

from django import forms
from django.forms import CheckboxSelectMultiple, RadioSelect
from .models import Item
from django.db.models import Count


class ItemFilter(django_filters.FilterSet):

    class Meta:
        model = Item
        fields = {
            'title': ['icontains'],
            'price': ['gte', 'lte'],
        }

    CHOICES_CREATED = (
        ('ascending_create','Primeras'),
        ('descending_create', 'Ultimas')
    )
    ordering_created = django_filters.ChoiceFilter(label='ordering_created', widget=forms.Select(attrs={'class': 'select-wrapper mdb-select md-form md-outline','onchange': 'this.form.submit();'}), choices=CHOICES_CREATED, method='filter_by_created')
    def filter_by_created(self, queryset, name, value):
        expression = 'created' if value == 'ascending_create' else '-created'
        return queryset.order_by(expression)


    CHOICES_TITLE = (
        ('ascending_title','A-Z'),
        ('descending_title', 'Z-A')
    )
    ordering_title = django_filters.ChoiceFilter(label='ordering_title', widget=forms.Select(attrs={'class': 'select-wrapper mdb-select md-form md-outline','onchange': 'this.form.submit();'}), choices=CHOICES_TITLE, method='filter_by_title')
    def filter_by_title(self, queryset, name, value):
        expression = 'title' if value == 'ascending_title' else '-title'
        return queryset.order_by(expression)


    CHOICES_PRICE = (
        ('ascending_price','Mayor Precio'),
        ('descending_price', 'Menor Precio')
    )
    ordering_price = django_filters.ChoiceFilter(label='ordering_price',  widget=forms.Select(attrs={'class': 'select-wrapper mdb-select md-form md-outline','onchange': 'this.form.submit();'}),choices=CHOICES_PRICE, method='filter_by_price')
    def filter_by_price(self, queryset, name, value):
        expression = 'price' if value == 'ascending_price' else '-price'
        return queryset.order_by(expression)

    
    CHOICES_DISCOUNT_PRICE = (
        ('ascending_discount','Mayor Descuento'),
        ('descending_discount', 'Menor Descuento')
    )
    ordering_discount_price = django_filters.ChoiceFilter(label='ordering_discount_price',  widget=forms.Select(attrs={'class': 'select-wrapper mdb-select md-form md-outline','onchange': 'this.form.submit();'}),choices=CHOICES_DISCOUNT_PRICE, method='filter_by_discount_price')
    def filter_by_discount_price(self, queryset, name, value):
        expression = 'discount_price' if value == 'ascending_discount' else '-discount_price'
        return queryset.order_by(expression)


    CHOICES_TOTAL = (
        ('ascending_price','Mayor Precio'),
        ('descending_price', 'Menor Precio'),
        ('ascending_title','A-Z'),
        ('descending_title', 'Z-A'),
        ('ascending_create','Primeras'),
        ('descending_create', 'Ultimas'),

        ('ascending_discount','Mayor Descuento'),
        ('descending_discount', 'Menor Descuento')
    )
    ordering_total = django_filters.ChoiceFilter(empty_label="Recomendados",label='ordering_total',  
    widget=forms.Select(attrs={'class': ' dropdown-select-order','onchange': 'this.form.submit();'}),
    choices=CHOICES_TOTAL, method='filter_by_total')
    def filter_by_total(self, queryset, name, value):
        if value == 'ascending_create':
            queryset = queryset.order_by('created')
        elif value == 'descending_create':
            queryset = queryset.order_by('-created')

        elif value == 'ascending_title':
            queryset = queryset.order_by('title')
        elif value == 'descending_title':
            queryset = queryset.order_by('-title')

        elif value == 'ascending_price':
            queryset = queryset.order_by('-price')
        elif value == 'descending_price':
            queryset = queryset.order_by('price')

        elif value == 'ascending_discount':
            queryset = queryset.order_by('-discount_price')
        elif value == 'descending_discount':
            queryset = queryset.order_by('discount_price')
        return queryset


