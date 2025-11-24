from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models, forms


class BrandListView(LoginRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 4

    def get_queryset(self):
        # Pega a empresa do usuário logado
        company = self.request.user.companyusers.company
        # Filtra as marcas para mostrar apenas as do usuário logado
        queryset = models.Brand.objects.filter(companyuser__company=company)

        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        company = self.request.user.companyusers.company
        context = super().get_context_data(**kwargs)
        context['company'] = company
        return context


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')

    def form_valid(self, form):
        form.instance.companyuser = self.request.user.companyusers
        return super().form_valid(form)


class BrandDetailView(LoginRequiredMixin, DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    success_url = reverse_lazy('brand_list')
