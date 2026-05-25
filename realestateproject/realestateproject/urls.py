from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
from django.urls import reverse

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

class HighSecurityAdminSite(admin.AdminSite):
    site_header = "EquiEstate Engine Secure Administration"
    site_title = "EquiEstate Admin Portal"
    index_title = "Site Administration"

    def each_context(self, request):
        context = super().each_context(request)
        logout_url = reverse('admin:logout')

        context['extrastyle'] = format_html(
            """
            <script>
                document.addEventListener("DOMContentLoaded", () => {{
                    const LOGOUT_URL = "{url}";
                    
                    function triggerImmediateSecurityLockdown() {{
                        window.location.href = LOGOUT_URL;
                    }}

                    document.addEventListener("visibilitychange", () => {{
                        if (document.visibilityState === "hidden") {{
                            triggerImmediateSecurityLockdown();
                        }}
                    }});

                    window.addEventListener("blur", () => {{
                        setTimeout(() => {{
                            if (document.activeElement === document.body || document.activeElement === null) {{
                                triggerImmediateSecurityLockdown();
                            }}
                        }}, 150);
                    }});
                }});
            </script>
            """,
            url=logout_url
        )
        return context

admin.site.__class__ = HighSecurityAdminSite

def root_routing_logic(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("/accounts/login/")

urlpatterns = [
    path('', root_routing_logic, name='root_redirect'),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    path("dashboard/", login_required(HomePageView.as_view()), name="home"),
    path("properties/", login_required(PropertiesDashboardView.as_view()), name="properties_view"),
    path("tenants/", login_required(TenantsRegistryView.as_view()), name="tenants_view"),
    path("ledger/", login_required(FinancialLedgerView.as_view()), name="ledger_view"),
    path("statistics/", login_required(StatisticsDashboardView.as_view()), name="statistics_view"),
    path("profile/", login_required(ProfileDashboardView.as_view()), name="profile_view"),
    
    path("utilities/calculate/", login_required(UtilityCalculatorView.as_view()), name="utility_calculator"),

    path("properties/add/", login_required(PropertyCreateView.as_view()), name="property_add"),
    path("properties/<int:pk>/edit/", login_required(PropertyUpdateView.as_view()), name="property_edit"),
    path("properties/<int:pk>/delete/", login_required(PropertyDeleteView.as_view()), name="property_delete"),

    path("tenants/add/", login_required(TenantCreateView.as_view()), name="tenant_add"),
    path("tenants/<int:pk>/edit/", login_required(TenantUpdateView.as_view()), name="tenant_edit"),
    path("tenants/<int:pk>/delete/", login_required(TenantDeleteView.as_view()), name="tenant_delete"),

    path("ledger/add/", login_required(TransactionCreateView.as_view()), name="transaction_add"),
    path("ledger/<int:pk>/edit/", login_required(TransactionUpdateView.as_view()), name="transaction_edit"),
    path("ledger/<int:pk>/delete/", login_required(TransactionDeleteView.as_view()), name="transaction_delete"),
]