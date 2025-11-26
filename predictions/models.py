from django.db import models
from companyusers.models import CompanyUser
from products.models import Product

class Notification(models.Model):
    company_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.company_user.company.name} - {self.product.name}'