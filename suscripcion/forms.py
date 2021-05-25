from django import forms
from .models import SuscripcionUsuario


class SuscripcionUsuarioForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'form-control'}
    ))
    class Meta:
        model = SuscripcionUsuario
        fields = ('email',)