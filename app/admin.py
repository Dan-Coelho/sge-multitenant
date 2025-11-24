from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserAdmin(BaseUserAdmin):

    def has_change_permission(self, request, obj=None):
        # Impede que não-superusuários editem superusuários
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Impede que não-superusuários deletem superusuários
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


# Re-registra o modelo User com o admin customizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
