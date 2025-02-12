import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Service

class SignUPForm(UserCreationForm):

    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'address')
    
    def generate_account_number(self):
        return str(uuid.uuid4().int)[:8]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.util_acc_no = self.generate_account_number()
        if commit:
            user.save()
        return user

class ServiceForm(forms.ModelForm):
    service_type = forms.CharField(required=True)
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = Service
        fields = ['service_type', 'description', 'files']