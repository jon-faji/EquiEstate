import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.cache import cache
from estateapp.models import Property, Tenant, Transaction, SystemProfile

# --- Dashboard & Registry Views ---

class PropertiesDashboardView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Property
    context_object_name = 'home'
    template_name = "property.html"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(address__icontains=query) | Q(property_type__icontains=query))
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['name', 'address', 'units', '-name', '-address', '-units']
        return qs.order_by(sort_by if sort_by in allowed_sorting else 'name')

class TenantsRegistryView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Tenant
    context_object_name = 'tenants'
    template_name = "tenant.html"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['last_name', 'created_at', '-last_name', '-created_at']
        return qs.order_by(sort_by if sort_by in allowed_sorting else ('last_name', 'created_at'))

class FinancialLedgerView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Transaction
    context_object_name = 'transactions'
    template_name = "transactions.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_currency = self.request.GET.get('currency', 'PHP')
        context['selected_currency'] = selected_currency
        total_amount = self.get_queryset().aggregate(Sum('amount'))['amount__sum'] or 0
        cache_key = f'rate_USD_to_{selected_currency}'
        rate = cache.get(cache_key)
        
        if rate is None:
            try:
                url = f'https://api.frankfurter.dev/v2/rates?base=USD&quotes={selected_currency}'
                response = requests.get(url, timeout=5)
                data = response.json()
                rate = next((item['rate'] for item in data if item['quote'] == selected_currency), 1.0)
                cache.set(cache_key, rate, 43200)
                context['api_error'] = False
            except Exception:
                rate = 1.0 
                context['api_error'] = True
        
        context['converted_total'] = round(float(total_amount) * float(rate), 2)
        return context

    def get_queryset(self):
        qs = super().get_queryset().select_related('tenant')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(status__icontains=query))
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['amount', 'date', '-amount', '-date']
        return qs.order_by(sort_by if sort_by in allowed_sorting else '-date')

# --- CRUD Views (Secured) ---

class PropertyCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Property
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('properties_view')

class TenantCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Tenant
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('tenants_view')

class TransactionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Transaction
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('ledger_view')

# --- Analytics & Profile ---

class StatisticsDashboardView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Property
    template_name = "statistics.html"

class ProfileDashboardView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Property
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = SystemProfile.objects.get_or_create(id=1)
        context['profile'] = profile
        return context

    def post(self, request, *args, **kwargs):
        profile, _ = SystemProfile.objects.get_or_create(id=1)
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        new_email = request.POST.get('admin_email')
        if new_email:
            profile.email = new_email
        profile.save()
        return redirect('profile_view')

# --- Home Page ---

class HomePageView(ListView):
    model = Property
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_properties'] = Property.objects.count()
        context['tenants_count'] = Tenant.objects.count()
        context['transactions_count'] = Transaction.objects.count()
        context['new_tenants_this_year'] = Tenant.objects.filter(
            created_at__year=timezone.now().year
        ).count()
        return context