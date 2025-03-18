from django.db import models



class ContractGenerator:
    def __init__(self, start_number=36):
        self.current_number = start_number - 1  # 36 dan boshlash uchun oldingi raqamni saqlaymiz

    def generate_contract_number(self):
        self.current_number += 1
        return f"TT{self.current_number}"

class Contract(models.Model):
    user = models.ForeignKey("botapp.BotUser", on_delete=models.SET_NULL, related_name="contracts", null=True, blank=True)
    contract_number = models.CharField(max_length=25, blank=True) 
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
    date = models.DateField(auto_now_add=True)
    pdf_file = models.FileField(upload_to="contracts/", null=True, blank=True)

    status_choices = (
        ("Draft", "Draft"),
        ("Signed", "Signed"),
        ("Rejected", "Rejected"),
    )
    status = models.CharField(max_length=25, choices=status_choices, default="Draft")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.contract_number:  # Agar contract_number bo‘sh bo‘lsa, yangi raqam yaratamiz
            last_contract = Contract.objects.order_by('-id').first()
            
            if last_contract and last_contract.contract_number.startswith("TT") and last_contract.contract_number[2:].isdigit():
                last_number = int(last_contract.contract_number[2:])
            else:
                last_number = 35  # TT36 dan boshlash uchun 35 ni olamiz

            self.contract_number = f"TT{last_number + 1}"
        
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.contract_number} - {self.company_name}"

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]
