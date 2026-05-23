from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from estateapp.models import Property, Tenant, Transaction

class PropertiesDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "property.html"
    paginate_by = 5                  

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(property_type__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['name', 'address', 'units', '-name', '-address', '-units']
        if sort_by in allowed_sorting:
            return qs.order_by(sort_by)
        return qs.order_by('name')

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

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['last_name', 'created_at', '-last_name', '-created_at']
        if sort_by in allowed_sorting:
            return qs.order_by(sort_by)
        return qs.order_by('last_name', 'created_at')

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

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(status__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['amount', 'date', '-amount', '-date']
        if sort_by in allowed_sorting:
            return qs.order_by(sort_by)
        return qs.order_by('-date')

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
        context['total_properties'] = Property.objects.count()
        context['tenants_count'] = Tenant.objects.count()
        context['transactions_count'] = Transaction.objects.count()
        
        today = timezone.now().date()
        context['new_tenants_this_year'] = Tenant.objects.filter(
            created_at__year=today.year
        ).count()
        
        return context

class StatisticsDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "statistics.html"    

class ProfileDashboardView(ListView):
    model = Property
    context_object_name = 'home'
    template_name = "profile.html"