import os
from django.core.management.base import BaseCommand
from django.conf import settings
from predictions.services import calculate_and_notify_stock
from companies.models import Company

class Command(BaseCommand):
    help = 'Calculates stock predictions for all companies and creates notifications.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting stock prediction calculation...'))
        
        # Fetch all companies
        companies = Company.objects.all()
        
        for company in companies:
            self.stdout.write(f'Calculating predictions for company: {company.name} (ID: {company.id})...')
            calculate_and_notify_stock(company.id)
            self.stdout.write(f'Finished predictions for company: {company.name}.')
            
        self.stdout.write(self.style.SUCCESS('Stock prediction calculation finished.'))
