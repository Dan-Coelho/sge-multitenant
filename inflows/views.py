from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms


class InflowListView(LoginRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 4

    def get_queryset(self):
        # Pega a empresa do usuário logado
        company = self.request.user.companyusers.company
        # Filtra as entradas para mostrar apenas as da empresa do usuário logado
        queryset = models.Inflow.objects.filter(companyuser__company=company)
        product = self.request.GET.get('product')

        if product:
            queryset = queryset.filter(product__title__icontains=product)
        return queryset

    def get_context_data(self, **kwargs):
        company = self.request.user.companyusers.company
        context = super().get_context_data(**kwargs)
        context['company'] = company
        return context


class InflowCreateView(LoginRequiredMixin, CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')

    def form_valid(self, form):
        form.instance.companyuser = self.request.user.companyusers
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(InflowCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class InflowDetailView(LoginRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail.html'
