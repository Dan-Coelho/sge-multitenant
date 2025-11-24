from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from app import metrics


class OutflowListView(LoginRequiredMixin, ListView):
    model = models.Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 4

    def get_queryset(self):
        # Pega a empresa do usuário logado
        company = self.request.user.companyusers.company
        # Filtra as saídas para mostrar apenas as da empresa do usuário logado
        queryset = models.Outflow.objects.filter(companyuser__company=company)

        product = self.request.GET.get('product')

        if product:
            queryset = queryset.filter(product__title__icontains=product)
        return queryset

    def get_context_data(self, **kwargs):
        company = self.request.user.companyusers.company
        context = super().get_context_data(**kwargs)
        context['sales_metrics'] = metrics.get_sales_metrics(company)
        context['company'] = company
        return context


class OutflowCreateView(LoginRequiredMixin, CreateView):
    model = models.Outflow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflow_list')

    def form_valid(self, form):
        form.instance.companyuser = self.request.user.companyusers
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OutflowCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class OutflowDetailView(LoginRequiredMixin, DetailView):
    model = models.Outflow
    template_name = 'outflow_detail.html'
