from django.db import models
from django.contrib.auth.models import User
from companies.models import Company


class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companyusers')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companyusers')

    def __str__(self):
        return self.user.username
