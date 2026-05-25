import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from estateapp.models import Property, Tenant, Transaction, SystemProfile

class SuperuserOrStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

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
        if sort_by in allowed_sorting:
            return qs.order_by(sort_by)
        return qs.order_by('last_name', 'created_at')

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
                rate = data.get('rates', {}).get(selected_currency, 1.0)
                cache.set(cache_key, rate, 43200)
                context['api_error'] = False
            except Exception:
                rate = 1.0 
                context['api_error'] = True
        
        context['converted_total'] = round(float(total_amount) * float(rate), 2)
        return context

    def get_queryset(self):
        qs = super().get_queryset().select_related('tenant', 'property')
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(status__icontains=query) | 
                Q(tenant__first_name__icontains=query) | 
                Q(tenant__last_name__icontains=query) |
                Q(property__name__icontains=query)
            )
            
        sort_by = self.request.GET.get('sort_by')
        allowed_sorting = ['amount', 'date', '-amount', '-date']
        return qs.order_by(sort_by if sort_by in allowed_sorting else '-date')

class PropertyCreateView(SuperuserOrStaffRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyUpdateView(SuperuserOrStaffRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Property
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('properties_view')

class PropertyDeleteView(SuperuserOrStaffRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Property
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('properties_view')

class TenantCreateView(SuperuserOrStaffRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantUpdateView(SuperuserOrStaffRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Tenant
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('tenants_view')

class TenantDeleteView(SuperuserOrStaffRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Tenant
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('tenants_view')

class TransactionCreateView(SuperuserOrStaffRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionUpdateView(SuperuserOrStaffRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    model = Transaction
    fields = '__all__'
    template_name = 'crud_form.html'
    success_url = reverse_lazy('ledger_view')

class TransactionDeleteView(SuperuserOrStaffRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Transaction
    template_name = 'crud_delete.html'
    success_url = reverse_lazy('ledger_view')

class StatisticsDashboardView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Property
    template_name = "statistics.html"

@method_decorator(csrf_protect, name='post')
class ProfileDashboardView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Property
    template_name = "settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = SystemProfile.objects.get_or_create(id=1)
        context['profile'] = profile
        return context

    def post(self, request, *args, **kwargs):
        profile, _ = SystemProfile.objects.get_or_create(id=1)
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()
            messages.success(request, 'Profile avatar updated successfully.')
            return redirect('profile_view')

        new_email = request.POST.get('admin_email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        email_audit = request.POST.get('email_audit') == 'on'
        live_cache = request.POST.get('live_cache') == 'on'

        if hasattr(profile, 'email_audit_reports'):
            profile.email_audit_reports = email_audit
        if hasattr(profile, 'live_engine_cache'):
            profile.live_engine_cache = live_cache
        profile.save()

        if new_email and new_email != request.user.email:
            request.user.email = new_email
            request.user.save()
            profile.profile_name = new_email.split('@')[0]
            profile.save()
            messages.success(request, 'Email identity updated successfully.')

        if current_password:
            if not request.user.check_password(current_password):
                messages.error(request, 'Verification failed. Cryptographic old password mismatch.')
            elif new_password or confirm_password:
                if new_password != confirm_password:
                    messages.error(request, 'Validation error. New password keys do not match.')
                elif len(new_password) < 8:
                    messages.error(request, 'Security failure. Password key length must be at least 8 characters.')
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Root security credentials updated successfully.')
            else:
                messages.success(request, 'System configuration preferences updated successfully.')
        else:
            if new_password or confirm_password:
                messages.error(request, 'Verification required. Please provide your current old password key.')

        return redirect('profile_view')

class UtilityCalculatorView(SuperuserOrStaffRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Tenant
    context_object_name = 'tenants'
    template_name = "utility_calculator.html"

    def post(self, request, *args, **kwargs):
        bill_type = request.POST.get('bill_type')  # 'ELECTRIC' o 'WATER'
        try:
            total_master_amount = float(request.POST.get('total_amount', 0))
        except ValueError:
            total_master_amount = 0.0
        
        if total_master_amount <= 0:
            messages.error(request, "Please enter a valid total bill amount.")
            return redirect('utility_calculator')

        tenants = Tenant.objects.all()
        total_system_consumption = 0.0
        tenant_data = []

        for tenant in tenants:
            if bill_type == 'ELECTRIC':
                consumed = tenant.current_electric_reading - tenant.previous_electric_reading
            else:
                consumed = tenant.current_water_reading - tenant.previous_water_reading
            
            if consumed < 0:
                messages.error(request, f"Error: Negative consumption detected for tenant {tenant.first_name} {tenant.last_name}. Check entries.")
                return redirect('utility_calculator')
                
            total_system_consumption += consumed
            tenant_data.append({'tenant': tenant, 'consumed': consumed})

        if total_system_consumption == 0:
            messages.error(request, "No consumption detected across all sub-meters. Cannot allocate costs.")
            return redirect('utility_calculator')

        rate_per_unit = total_master_amount / total_system_consumption

        transactions_created = 0
        for data in tenant_data:
            tenant = data['tenant']
            consumption = data['consumed']
            tenant_share = round(consumption * rate_per_unit, 2)
            
            if tenant_share > 0:
                Transaction.objects.create(
                    tenant=tenant,
                    amount=tenant_share,
                    status='UNPAID',
                    date=timezone.now().date(),
                    property=getattr(tenant, 'property', None)
                )
                
                if bill_type == 'ELECTRIC':
                    tenant.previous_electric_reading = tenant.current_electric_reading
                else:
                    tenant.previous_water_reading = tenant.current_water_reading
                tenant.save()
                
                transactions_created += 1

        messages.success(request, f"Successfully calculated utility! Distributed PHP {total_master_amount} across {transactions_created} accounts.")
        return redirect('ledger_view')

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