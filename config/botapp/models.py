from django.db import models


# Bot foydalanuvchilari uchun model
class BotUser(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name}'