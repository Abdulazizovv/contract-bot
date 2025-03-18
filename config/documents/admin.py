from django.contrib import admin
from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "company_name", "total_price", "monthly_payment", "date", "created_at", "updated_at"]
    list_display_links = ["id", "company_name"]
    search_fields = ["company_name", "total_price", "monthly_payment", "date"]
    list_filter = ["company_name", "total_price", "monthly_payment", "date"]
    list_per_page = 25


admin.site.register(Contract, ContractAdmin)