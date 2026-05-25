from django.contrib import admin
from .models import Property, Tenant, Transaction

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "property_type", "units", "created_at")
    search_fields = ("name", "address")
    list_filter = ("property_type", "created_at")

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "get_assigned_property", "rent_amount", "lease_end")
    search_fields = ("last_name", "first_name", "email")
    list_filter = ("lease_end",)

    def get_assigned_property(self, obj):
        return obj.property.name if obj.property else "Vacant / Unassigned"
    get_assigned_property.short_description = 'Assigned Asset'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("property", "tenant", "amount", "date", "status")
    search_fields = ("property__name", "tenant__last_name", "status")
    list_filter = ("status", "date") 