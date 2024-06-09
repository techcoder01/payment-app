from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    card_holder_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=25)
    ifsc_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    bank_country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    ACCOUNT_TYPE_CHOICES = [
        ("personal", "Personal"),
        ("business", "Business"),
    ]
    account_type = models.CharField(
        max_length=20, choices=ACCOUNT_TYPE_CHOICES, default="Personal"
    )
