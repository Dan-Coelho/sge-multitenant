from django.db import models
from companyusers.models import CompanyUser
from brands.models import Brand


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    companyuser = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    cost_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
