from django.db import models
from datetime import datetime


class Contract(models.Model):
    user = models.ForeignKey("botapp.BotUser", on_delete=models.SET_NULL, related_name="contracts", null=True, blank=True)
    director_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
    monthly_payment = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_account = models.CharField(max_length=255, null=True, blank=True)
    company_bank = models.CharField(max_length=255, null=True, blank=True)
    company_mfo = models.CharField(max_length=15, null=True, blank=True)
    company_inn = models.CharField(max_length=15, null=True, blank=True)
    company_oked = models.CharField(max_length=15, null=True, blank=True)
    company_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=datetime.now().strftime("%Y-%m-%d"))
    pdf_file = models.FileField(upload_to="contracts/", null=True, blank=True)

    status_choices = (
        ("Draft", "Draft"),
        ("Signed", "Signed"),
        ("Rejected", "Rejected"),
    )
    status = models.CharField(max_length=25, choices=status_choices, default="Draft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]
