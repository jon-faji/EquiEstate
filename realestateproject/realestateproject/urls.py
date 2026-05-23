from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from estateapp.views import (
    FinancialLedgerView,
    HomePageView,
    ProfileDashboardView,
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


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Main Pages
    path("", HomePageView.as_view(), name="home"),
    path("properties/", PropertiesDashboardView.as_view(), name="properties_view"),
    path("tenants/", TenantsRegistryView.as_view(), name="tenants_view"),
    path("ledger/", FinancialLedgerView.as_view(), name="ledger_view"),
    path("statistics/", StatisticsDashboardView.as_view(), name="statistics_view"),
    path("profile/", ProfileDashboardView.as_view(), name="profile_view"),

    # Authentication
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Property Management
    path("properties/add/", PropertyCreateView.as_view(), name="property_add"),
    path(
        "properties/<int:pk>/edit/",
        PropertyUpdateView.as_view(),
        name="property_edit",
    ),
    path(
        "properties/<int:pk>/delete/",
        PropertyDeleteView.as_view(),
        name="property_delete",
    ),

    # Tenant Management
    path("tenants/add/", TenantCreateView.as_view(), name="tenant_add"),
    path(
        "tenants/<int:pk>/edit/",
        TenantUpdateView.as_view(),
        name="tenant_edit",
    ),
    path(
        "tenants/<int:pk>/delete/",
        TenantDeleteView.as_view(),
        name="tenant_delete",
    ),

    # Financial Transactions
    path("ledger/add/", TransactionCreateView.as_view(), name="transaction_add"),
    path(
        "ledger/<int:pk>/edit/",
        TransactionUpdateView.as_view(),
        name="transaction_edit",
    ),
    path(
        "ledger/<int:pk>/delete/",
        TransactionDeleteView.as_view(),
        name="transaction_delete",
    ),
]