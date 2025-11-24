from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from .models import CompanyUser


# 1. Crie um "Inline" para CompanyUser
# Isso permite que você edite o CompanyUser DENTRO do formulário do User.
class CompanyUserInline(admin.StackedInline):
    model = CompanyUser
    can_delete = False
    verbose_name_plural = 'Empresa Associada'
    fk_name = 'user'
    # Oculta o campo 'company' do formulário inline, pois será preenchido automaticamente.
    exclude = ('company',)


# 2. Crie um UserAdmin customizado para o portal do cliente
class UserCompanyAdmin(BaseUserAdmin):
    # Adiciona o inline ao formulário de User
    inlines = (CompanyUserInline,)
    list_display = ('username', 'first_name', 'last_name', 'is_active')

    # Remove permissões e grupos do formulário do User, o gerente não deve gerenciá-los
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Status', {'fields': ('is_active',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets

    def get_queryset(self, request):
        """
        Mostra na lista apenas os usuários que pertencem à empresa do gerente.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.exclude(is_superuser=True)

        try:
            user_company = request.user.companyusers.company
            return qs.filter(companyusers__company=user_company).exclude(is_superuser=True)
        except CompanyUser.DoesNotExist:
            return qs.none()

    def save_related(self, request, form, formsets, change):
        """
        Este método é chamado após o salvamento do objeto principal (User).
        É o local ideal para preencher dados no inline (CompanyUser) antes de salvá-lo.
        """
        # Primeiro, execute o comportamento padrão para salvar o formulário principal
        super().save_related(request, form, formsets, change)

        # 'form.instance' é o objeto User que acabamos de salvar
        user_instance = form.instance

        # Se for um novo usuário, associe a empresa
        # O 'try-except' evita erros se o usuário já tiver um companyuser (caso de edição)
        try:
            # Se companyusers já existe, não faz nada
            _ = user_instance.companyusers
        except CompanyUser.DoesNotExist:
            # Se não existe, cria um novo CompanyUser associado ao User
            # e à empresa do gerente que o está criando.
            CompanyUser.objects.create(
                user=user_instance,
                company=request.user.companyusers.company
            )


# Admin Principal (/admin/)
# Registra o CompanyUser da forma padrão para o superusuário
class CompanyUserGlobalAdmin(admin.ModelAdmin):
    list_display = ('user', 'company')
    list_filter = ('company',)
    search_fields = ('user__username', 'company__name')


# Garante que o modelo não está duplamente registrado
try:
    admin.site.unregister(CompanyUser)
except admin.sites.NotRegistered:
    pass
admin.site.register(CompanyUser, CompanyUserGlobalAdmin)
