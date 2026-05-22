from django.core.management.base import BaseCommand
from faker import Faker
from estateapp.models import Property, Tenant, Transaction
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate mock data for EquiEstate portfolio testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # 1. Create Properties
        prop_types = ['residential', 'commercial', 'industrial']
        properties = []
        for _ in range(12):
            p = Property.objects.create(
                name=f"{fake.city()} {random.choice(['Tower', 'Plaza', 'Manor', 'Complex'])}",
                address=fake.address().replace('\n', ', '),
                property_type=random.choice(prop_types),
                units=random.randint(1, 10)
            )
            properties.append(p)
        self.stdout.write(self.style.SUCCESS('Created 12 custom properties.'))

        # 2. Create Tenants & link them to properties
        tenants = []
        for prop in properties:
            # Leave a couple properties empty to test vacancy tracking logic later
            if random.random() < 0.2:
                continue
                
            start_date = fake.date_between(start_date="-1y", end_date="today")
            end_date = start_date + timedelta(days=365)
            
            t = Tenant.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                property=prop,
                lease_start=start_date,
                lease_end=end_date,
                rent_amount=random.choice([1200.00, 1500.00, 2200.00, 3500.00])
            )
            tenants.append(t)
        self.stdout.write(self.style.SUCCESS('Successfully linked tenants to assets.'))

        # 3. Create Historical Ledger Transactions
        for tenant in tenants:
            for i in range(5): # Generate 5 months of rent history per tenant
                Transaction.objects.create(
                    property=tenant.property,
                    tenant=tenant,
                    amount=tenant.rent_amount,
                    date=fake.date_between(start_date="-5m", end_date="today"),
                    status=random.choice(['Paid', 'Paid', 'Paid', 'Pending', 'Overdue'])
                )
        self.stdout.write(self.style.SUCCESS('Financial ledger populated successfully.'))