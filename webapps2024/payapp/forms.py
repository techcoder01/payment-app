# forms.py

from django import forms
from .models import BankAccount, Card

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)  # Assuming max length for phone number
    

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_type', 'card_number', 'expiry_date', 'cvv', 'card_holder_name']

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name', 'account_number', 'ifsc_code', 'bank_name', 'account_type', 'bank_country']
