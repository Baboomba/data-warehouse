from django.db import models

class Info(models.Model):
    product_id = models.CharField(max_length=20)
    product_name = models.CharField(max_length=150)
    monthly_premium = models.IntegerField()
    policy_id = models.CharField(unique=True, max_length=20)
    model_name = models.CharField(max_length=15)
    user_name = models.CharField(max_length=150)
    user_contact = models.CharField(max_length=30)
    user_birth = models.CharField(max_length=30)
    imei = models.BigIntegerField(null=True)
    serial_number = models.CharField(max_length=20, null=True)
    initial_call = models.DateField(null=True)
    date_joined = models.DateField()
    date_closed = models.DateField(null=True)
    insurance_company = models.CharField(max_length=5, null=True)
    insurance_status = models.CharField(max_length=10, null=True)
    untact_solution = models.BigIntegerField(null=True)
    is_promoted = models.CharField(max_length=5, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['date_joined']),
        ]
    
    def __str__(self):
        return self.policy_id