from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from app.company_admin import company_admin_site

# Garante que apenas superusuários possam acessar a rota /admin/
admin.site.has_permission = lambda r: r.user.is_superuser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', company_admin_site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.home, name='home'),

    path('', include('brands.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path('', include('products.urls')),
    path('', include('predictions.urls')),
]
