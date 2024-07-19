from .models import Costumer
from django import forms

class CostumerForm(forms.ModelForm):
    class Meta:
        model = Costumer
        fields = ['first_name', 'last_name','style']
        
    first_name = forms.CharField(label='Nombres del Cliente')
    last_name = forms.CharField(label='Apellidos del Cliente')
    style = forms.CharField(label='Estilo')