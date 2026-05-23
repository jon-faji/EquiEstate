from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from estateapp.models import Property, Tenant, Transaction

class PropertiesDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "property.html"
    paginate_by = 5                  

class PropertyCreateView(CreateView):
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyUpdateView(UpdateView):
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('properties_view')

class TenantsRegistryView(ListView):
    model = Tenant
    context_object_name = 'tenants'
    template_name = "tenant.html"
    paginate_by = 5                  

class TenantCreateView(CreateView):
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantUpdateView(UpdateView):
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantDeleteView(DeleteView):
    model = Tenant
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('tenants_view')

class FinancialLedgerView(ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = "transactions.html" 
    paginate_by = 5                  

class TransactionCreateView(CreateView):
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionUpdateView(UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('ledger_view')

class HomePageView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "home.html"         

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenants_count'] = Tenant.objects.count()
        context['transactions_count'] = Transaction.objects.count()
        return context

class StatisticsDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "statistics.html"    

class ProfileDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "profile.html"