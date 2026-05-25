from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from estateapp.views import (
    FinancialLedgerView,
    HomePageView,
    ProfileDashboardView,
    UtilityCalculatorView, 
    PropertiesDashboardView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyUpdateView,
    StatisticsDashboardView,
    TenantCreateView,
    TenantDeleteView,
    TenantUpdateView,
    TenantsRegistryView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionUpdateView,
)

def root_routing_logic(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("/accounts/login/")

urlpatterns = [
    
    path('', root_routing_logic, name='root_redirect'),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    # Core Application Panels Workspace
    path("dashboard/", login_required(HomePageView.as_view()), name="home"),
    path("properties/", login_required(PropertiesDashboardView.as_view()), name="properties_view"),
    path("tenants/", login_required(TenantsRegistryView.as_view()), name="tenants_view"),
    path("ledger/", login_required(FinancialLedgerView.as_view()), name="ledger_view"),
    path("statistics/", login_required(StatisticsDashboardView.as_view()), name="statistics_view"),
    path("profile/", login_required(ProfileDashboardView.as_view()), name="profile_view"),
    
    # Utility Cost Allocation Engine
    path("utilities/calculate/", login_required(UtilityCalculatorView.as_view()), name="utility_calculator"),

    # Property Allocation Pipelines (CRUD Operations)
    path("properties/add/", login_required(PropertyCreateView.as_view()), name="property_add"),
    path("properties/<int:pk>/edit/", login_required(PropertyUpdateView.as_view()), name="property_edit"),
    path("properties/<int:pk>/delete/", login_required(PropertyDeleteView.as_view()), name="property_delete"),

    # Tenant Records Management (CRUD Operations)
    path("tenants/add/", login_required(TenantCreateView.as_view()), name="tenant_add"),
    path("tenants/<int:pk>/edit/", login_required(TenantUpdateView.as_view()), name="tenant_edit"),
    path("tenants/<int:pk>/delete/", login_required(TenantDeleteView.as_view()), name="tenant_delete"),

    # Financial Transaction Ledgers (CRUD Operations
    path("ledger/add/", login_required(TransactionCreateView.as_view()), name="transaction_add"),
    path("ledger/<int:pk>/edit/", login_required(TransactionUpdateView.as_view()), name="transaction_edit"),
    path("ledger/<int:pk>/delete/", login_required(TransactionDeleteView.as_view()), name="transaction_delete"),
]