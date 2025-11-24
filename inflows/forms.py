from django import forms
from . import models
from products.models import Product


class InflowForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Pega o usuário que foi passado pela view
        user = kwargs.pop('user', None)
        super(InflowForm, self).__init__(*args, **kwargs)

        # Filtra o queryset do campo 'brand'
        if user:
            self.fields['product'].queryset = Product.objects.filter(companyuser=user.companyusers)

    class Meta:
        model = models.Inflow
        fields = ['product', 'quantity', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição'
        }
