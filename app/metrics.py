from django.db.models import Sum, F
from datetime import timedelta
from django.utils import timezone
from products.models import Product
from outflows.models import Outflow
from brands.models import Brand


def get_product_metrics(company):
    """Calcula as métricas de produtos para uma EMPRESA específica."""
    products = Product.objects.filter(companyuser__company=company)

    metrics = products.aggregate(
        total_quantity=Sum('quantity'),
        total_cost_price=Sum(F('quantity') * F('cost_price')),
        total_selling_price=Sum(F('quantity') * F('selling_price'))
    )

    total_quantity = metrics['total_quantity'] or 0
    total_cost_price = metrics['total_cost_price'] or 0
    total_selling_price = metrics['total_selling_price'] or 0
    total_profit = total_selling_price - total_cost_price

    return {
        'total_cost_price': f'R$ {total_cost_price:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        'total_selling_price': f'R$ {total_selling_price:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        'total_quantity': total_quantity,
        'total_profit': f'R$ {total_profit:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
    }


def get_sales_metrics(company):
    """Calcula as métricas de vendas para uma EMPRESA específica."""
    sales = Outflow.objects.filter(companyuser__company=company)

    metrics = sales.aggregate(
        total_sales=Sum('quantity'),
        total_sales_value=Sum(F('quantity') * F('product__selling_price')),
        total_sales_cost=Sum(F('quantity') * F('product__cost_price'))
    )
    total_products_sold = metrics['total_sales'] or 0
    total_sales_value = metrics['total_sales_value'] or 0
    total_sales_cost = metrics['total_sales_cost'] or 0
    total_sales_profit = total_sales_value - total_sales_cost

    return {
        'total_sales': sales.count(),
        'total_products_sold': total_products_sold,
        'total_sales_value': f'R$ {total_sales_value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        'total_sales_profit': f'R$ {total_sales_profit:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
    }


def get_daily_sales_data(company):
    """Retorna dados de vendas diárias (valor) para uma EMPRESA."""
    seven_days_ago = timezone.now() - timedelta(days=6)
    sales = Outflow.objects.filter(companyuser__company=company, created_at__date__gte=seven_days_ago.date()) \
        .annotate(date=F('created_at__date')) \
        .values('date') \
        .annotate(daily_value=Sum(F('quantity') * F('product__selling_price'))) \
        .order_by('date')

    sales_dict = {sale['date'].strftime('%Y-%m-%d'): float(sale['daily_value']) for sale in sales}
    dates = [(timezone.now().date() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    values = [sales_dict.get(date, 0) for date in dates]

    return {'dates': [d[8:] + '/' + d[5:7] for d in dates], 'values': values}


def get_daily_sales_quantity_data(company):
    """Retorna dados de vendas diárias (quantidade) para uma EMPRESA."""
    seven_days_ago = timezone.now() - timedelta(days=6)
    sales = Outflow.objects.filter(companyuser__company=company, created_at__date__gte=seven_days_ago.date()) \
        .annotate(date=F('created_at__date')) \
        .values('date') \
        .annotate(daily_quantity=Sum('quantity')) \
        .order_by('date')

    sales_dict = {sale['date'].strftime('%Y-%m-%d'): sale['daily_quantity'] for sale in sales}
    dates = [(timezone.now().date() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    values = [sales_dict.get(date, 0) for date in dates]

    return {'dates': [d[8:] + '/' + d[5:7] for d in dates], 'values': values}


def get_product_count_by_brand(company):
    """Retorna a contagem de produtos por marca para uma EMPRESA."""
    brands = Brand.objects.filter(companyuser__company=company).prefetch_related('products')
    return {brand.name: brand.products.count() for brand in brands}
