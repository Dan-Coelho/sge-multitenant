from django.db.models import Avg, Sum
from datetime import date, timedelta
from products.models import Product
from outflows.models import Outflow
from .models import Notification
from companyusers.models import CompanyUser

def calculate_and_notify_stock(company_id):
    company_users = CompanyUser.objects.filter(company__id=company_id)
    if not company_users.exists():
        return

    # Assuming all CompanyUsers for a company share the same products
    # We'll use the first company_user to filter products and outflows
    # This might need refinement if product visibility differs per user within a company
    company_user_instance = company_users.first()

    # Get all products associated with the company
    products = Product.objects.filter(companyuser__company=company_user_instance.company)

    for product in products:
        # Calculate average daily outflow for the last 30 days
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_outflows = Outflow.objects.filter(
            companyuser__company=company_user_instance.company,
            product=product,
            created_at__gte=thirty_days_ago
        )

        total_outflow_quantity = recent_outflows.aggregate(Sum('quantity'))['quantity__sum'] or 0
        days_with_outflow = recent_outflows.values('created_at__date').distinct().count()

        if days_with_outflow > 0:
            average_daily_outflow = total_outflow_quantity / days_with_outflow
        else:
            average_daily_outflow = 0

        # Calculate sufficient stock for 1 week (7 days)
        sufficient_stock_for_one_week = average_daily_outflow * 7

        # Check if current stock is below the sufficient level
        if product.quantity < sufficient_stock_for_one_week and sufficient_stock_for_one_week > 0:
            message = f"O estoque do produto '{product.title}' está baixo. Recomendamos comprar mais {sufficient_stock_for_one_week - product.quantity:.0f} unidades para ter estoque suficiente para 1 semana."
            
            # Create a notification for each company user associated with the company
            for cu in company_users:
                Notification.objects.create(
                    company_user=cu,
                    product=product,
                    message=message
                )

        elif sufficient_stock_for_one_week == 0 and product.quantity == 0 and total_outflow_quantity > 0:
            message = f"O produto '{product.title}' não teve saídas nos últimos 30 dias, mas está com estoque zerado e teve saídas anteriores. Considere comprar mais para evitar a falta."
            for cu in company_users:
                Notification.objects.create(
                    company_user=cu,
                    product=product,
                    message=message
                )
