from django.contrib import admin
from products.models import Product


# Admin customizado para o portal da empresa
class ProductCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'cost_price', 'selling_price', 'quantity', 'created_at')
    search_fields = ('title', 'brand__name')
    list_filter = ('brand',)

    def get_queryset(self, request):
        """
        Filtra o queryset para mostrar apenas os produtos
        da empresa do usuário logado.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        # Filtra produtos pelo companyuser associado ao user logado
        return qs.filter(companyuser__user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Ao criar um novo produto, associa-o automaticamente
        ao companyuser do usuário logado.
        """
        if not obj.pk:  # Apenas na criação
            if not request.user.is_superuser:
                try:
                    # Assumindo que o CompanyUser já foi criado para este User
                    obj.companyuser = request.user.companyusers
                except AttributeError:
                    # Tratar caso o companyuser não exista, se necessário
                    pass
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Remove o campo 'companyuser' do formulário, pois ele será
        preenchido automaticamente.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'companyuser' in form.base_fields:
                del form.base_fields['companyuser']
        return form


# Admin padrão para o superusuário (opcional, mas recomendado)
# Isso permite que você veja TODOS os produtos no admin principal
class ProductGlobalAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'companyuser', 'cost_price', 'selling_price', 'created_at')
    search_fields = ('title', 'brand__name', 'companyuser__user__username')
    list_filter = ('brand', 'companyuser__company__name')


admin.site.register(Product, ProductGlobalAdmin)
