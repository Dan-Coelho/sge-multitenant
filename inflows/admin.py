from django.contrib import admin
from .models import Inflow
from companyusers.models import CompanyUser


class InflowCompanyAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'companyuser', 'created_at')
    exclude = ('companyuser',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            user_company = request.user.companyusers.company
            return qs.filter(companyuser__company=user_company)
        except CompanyUser.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_superuser:
                obj.companyuser = request.user.companyusers
        super().save_model(request, obj, form, change)


class InflowGlobalAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'companyuser', 'created_at')
    list_filter = ('companyuser__company__name',)


admin.site.register(Inflow, InflowGlobalAdmin)
