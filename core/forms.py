from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Perfil, UserProfile, Token_tbk

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('W', 'Webpay')
)
class CheckoutForm(forms.Form):
    shipping_address1 = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(Selecciona tu ciudad)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address1 = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(Selecciona tu ciudad)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-3"',
        'placeholder': 'Código Cupón',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4
    }))
    email = forms.EmailField()

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class UserProfileForm(forms.ModelForm):

    user = forms.CharField(required=False,label='user',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    first_name = forms.CharField(required=False,label='first_name',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    last_name = forms.CharField(required=False,label='last_name',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    street_address = forms.CharField(required=False,label='street_address',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    apartment_address = forms.CharField(required=False, label='apartment_address',widget=forms.TextInput(
        attrs={'class':'form-control','required': 'false'} 
    ))
    email = forms.EmailField(required=False,widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))

    phone = forms.CharField(required=False,label='phone',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    order_notes = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'cols': '5', 'rows': '10', 'class': 'form-control','required': 'false'} 

    ))


    class Meta:
        model = UserProfile
        fields = [
            'user',
            'first_name',
            'last_name',
            'street_address',
            'apartment_address',
            'email',
            'phone',
            'order_notes'
        ]

class PerfilForm(forms.ModelForm):

    city = forms.CharField(label='city',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    first_name = forms.CharField(label='first_name',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    last_name = forms.CharField(label='last_name',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    street_address = forms.CharField(label='street_address',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    apartment_address = forms.CharField(label='apartment_address',widget=forms.TextInput(
        attrs={'class':'form-control','required': 'false'} 
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))

    phone = forms.CharField(label='phone',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    order_notes = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'cols': '5', 'rows': '10', 'class': 'form-control','required': 'false'} 

    ))
    class Meta:
        model = Perfil
        fields = [
            'city',
            'first_name',
            'last_name',
            'street_address',
            'apartment_address',
            'email',
            'phone',
            'order_notes'
        ]

class TokenForm(forms.ModelForm):
    transbank_tkn = forms.CharField(label='transbank_tkn',widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

    class Meta:
        model = Token_tbk
        fields = [
            'transbank_tkn',
        ]


