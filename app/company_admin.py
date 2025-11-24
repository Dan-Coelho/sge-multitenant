from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from brands.models import Brand
from products.models import Product
from inflows.models import Inflow
from outflows.models import Outflow

# Importa as classes ModelAdmin customizadas de cada app
from brands.admin import BrandCompanyAdmin
from products.admin import ProductCompanyAdmin
from inflows.admin import InflowCompanyAdmin
from outflows.admin import OutflowCompanyAdmin
from companyusers.admin import UserCompanyAdmin


class CompanyAdminSite(AdminSite):
    site_header = 'Portal Administrativo da Empresa'
    site_title = 'Portal da Empresa'
    index_title = 'Bem-vindo ao Portal da sua Empresa'


company_admin_site = CompanyAdminSite(name='company_admin')

# --- REGISTRO CENTRALIZADO PARA O PORTAL ---
# Registra todos os modelos que o cliente deve poder gerenciar

# Gestão de usuários (colaboradores)
company_admin_site.register(User, UserCompanyAdmin)

# Gestão de Marcas e Produtos
company_admin_site.register(Brand, BrandCompanyAdmin)
company_admin_site.register(Product, ProductCompanyAdmin)

# Gestão de Entradas e Saídas
company_admin_site.register(Inflow, InflowCompanyAdmin)
company_admin_site.register(Outflow, OutflowCompanyAdmin)
