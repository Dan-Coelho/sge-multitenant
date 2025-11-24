import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import metrics


@login_required(login_url='login')
def home(request):
    try:
        company = request.user.companyusers.company
    except AttributeError:
        # Se o usuário não tem uma empresa (ex: superuser não associado),
        # retorne um contexto vazio ou uma mensagem.
        return render(request, 'home.html', {'error': 'Usuário não associado a uma empresa.'})

    product_metrics = metrics.get_product_metrics(company)
    sales_metrics = metrics.get_sales_metrics(company)
    daily_sales_data = metrics.get_daily_sales_data(company)
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data(company)
    product_count_by_brand = metrics.get_product_count_by_brand(company)
    context = {
        'product_metrics': product_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),
        'daily_sales_quantity_data': json.dumps(daily_sales_quantity_data),
        'product_count_by_brand': json.dumps(product_count_by_brand),
        'company': company
    }

    return render(request, 'home.html', context)
