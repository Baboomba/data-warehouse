from django.db import models

class Info(models.Model):
    product_info = models.CharField(max_length=20)
    product_name = models.CharField(max_length=150)
    monthly_premium = models.IntegerField()
    policy_id = models.CharField(unique=True, max_length=20)
    model_name = models.CharField(max_length=15)
    user_name = models.CharField(max_length=150)
    user_contact = models.CharField(max_length=30)
    user_birth = models.CharField(max_length=30)
    imei = models.IntegerField()
    serial_number = models.IntegerField()
    initial_call = models.DateField()
    date_joined = models.DateField()
    date_closed = models.DateField()
    insurance_company = models.CharField(max_length=5)
    insurance_status = models.CharField(max_length=10)
    untact_solution = models.IntegerField()
    is_promoted = models.CharField(max_length=5)
    
    def __str__(self):
        return self.policy_id