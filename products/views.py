from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from brands.models import Brand
from app import metrics


class ProductListView(LoginRequiredMixin, ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        # Pega a emprea do usuário logado
        company = self.request.user.companyusers.company
        # Filtra os produtos para mostrar apenas os da empresa do usuário logado
        queryset = models.Product.objects.filter(companyuser__company=company)

        title = self.request.GET.get('title')
        brand = self.request.GET.get('brand')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        return queryset

    def get_context_data(self, **kwargs):
        company = self.request.user.companyusers.company
        context = super().get_context_data(**kwargs)
        context['product_metrics'] = metrics.get_product_metrics(company)
        context['brands'] = Brand.objects.all()
        context['company'] = company
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.companyuser = self.request.user.companyusers
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = models.Product
    template_name = 'product_detail.html'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Product
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
