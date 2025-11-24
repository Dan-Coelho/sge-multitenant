from django.contrib import admin
from .models import Brand
from companyusers.models import CompanyUser


# Admin customizado para o portal da empresa
class BrandCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'companyuser', 'created_at')
    search_fields = ('name',)
    exclude = ('companyuser',)  # Oculta o campo do formulário

    def get_queryset(self, request):
        """
        Filtra para mostrar apenas as marcas cuja empresa do criador
        é a mesma empresa do usuário logado.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        try:
            user_company = request.user.companyusers.company
            return qs.filter(companyuser__company=user_company)
        except CompanyUser.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        """
        Ao criar uma nova marca, associa-a automaticamente
        ao companyuser do usuário logado.
        """
        if not change:  # Apenas na criação
            if not request.user.is_superuser:
                try:
                    obj.companyuser = request.user.companyusers
                except CompanyUser.DoesNotExist:
                    pass
        super().save_model(request, obj, form, change)


# Admin padrão para o superusuário (no /admin/)
class BrandGlobalAdmin(admin.ModelAdmin):
    list_display = ('name', 'companyuser', 'get_company')
    list_filter = ('companyuser__company__name',)
    search_fields = ('name', 'companyuser__user__username')

    @admin.display(description='Company')
    def get_company(self, obj):
        return obj.companyuser.company


admin.site.register(Brand, BrandGlobalAdmin)
