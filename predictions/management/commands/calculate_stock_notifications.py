from django.core.management.base import BaseCommand
from django.db import transaction
from companies.models import Company
from predictions.services import calculate_and_notify_stock

class Command(BaseCommand):
    help = 'Calculates stock predictions and creates notifications for all companies.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting stock prediction calculation and notification generation...'))
        
        companies = Company.objects.all()
        for company in companies:
            with transaction.atomic():
                self.stdout.write(f'Processing company: {company.name} (ID: {company.id})')
                try:
                    calculate_and_notify_stock(company.id)
                    self.stdout.write(self.style.SUCCESS(f'Successfully processed company {company.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing company {company.name}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Stock prediction calculation and notification generation finished.'))
