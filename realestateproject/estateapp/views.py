from django.shortcuts import render
from django.views.generic.list import ListView
from estateapp.models import Property, Tenant, Transaction

class HomePageView(ListView):
    # Pulls our property objects to display within our dashboard table view
    model = Property
    context_object_name = 'home'
    template_name = "home.html"

class PropertiesDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "property.html"

class TenantsRegistryView(ListView):
    model = Tenant
    context_object_name = 'tenants'
    template_name = "tenant.html"

class FinancialLedgerView(ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = "transactions.html"

class StatisticsDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "statistics.html"

class ProfileDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "profile.html"