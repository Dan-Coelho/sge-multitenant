from django import forms
from django.core.exceptions import ValidationError
from . import models
from products.models import Product


class OutflowForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Pega o usuário que foi passado pela view
        user = kwargs.pop('user', None)
        super(OutflowForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['product'].queryset = Product.objects.filter(companyuser=user.companyusers)

    class Meta:
        model = models.Outflow
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

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        if quantity and product:
            if quantity > product.quantity:
                raise ValidationError(
                    f'A quantidade disponível em estoque para o produto {product.title} é de {product.quantity} unidades'
                )
        return cleaned_data
