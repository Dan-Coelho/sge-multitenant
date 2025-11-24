from django.db import models
from companyusers.models import CompanyUser
from products.models import Product


class Outflow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='outflows')
    companyuser = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='outflows')
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.product)
