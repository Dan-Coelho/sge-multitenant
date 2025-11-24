from django import forms
from . import models
from brands.models import Brand


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Pega o usuário que foi passado pela view
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        # Filtra o queryset do campo 'brand'
        if user:
            self.fields['brand'].queryset = Brand.objects.filter(companyuser=user.companyusers)

    class Meta:
        model = models.Product
        fields = ['title', 'brand', 'description', 'cost_price', 'selling_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título',
            'brand': 'Marca',
            'description': 'Descrição',
            'cost_price': 'Preço de Custo',
            'selling_price': 'Preço de Venda',
        }
