from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('company_user', 'product', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at', 'company_user__company')
    search_fields = ('company_user__user__username', 'product__name', 'message')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marcar notificações selecionadas como lidas"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Marcar notificações selecionadas como não lidas"