from django.contrib import admin
from django.urls import path
from estateapp.views import HomePageView, PropertiesDashboardView, TenantsRegistryView, FinancialLedgerView, StatisticsDashboardView, ProfileDashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('properties/', PropertiesDashboardView.as_view(), name='properties_view'),
    path('tenants/', TenantsRegistryView.as_view(), name='tenants_view'),
    path('ledger/', FinancialLedgerView.as_view(), name='ledger_view'),
    path('statistics/', StatisticsDashboardView.as_view(), name='statistics_view'),
    path('profile/', ProfileDashboardView.as_view(), name='profile_view'),
    
]