from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    # keeping username optional
    username = models.CharField(max_length=150, null=True, blank=True, unique=False)
    
    # Required fields
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits"
    )
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        validators=[phone_regex],
        unique=True
    )
    address = models.TextField()
    util_acc_no = models.CharField(
        max_length=20,
        unique=True,
    )
    
    # Additional useful fields
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number',  'address', ]

    def __str__(self):
        return f"{self.full_name} - {self.util_acc_no}"

    def save(self, *args, **kwargs):
        """Automatically set username to email if not provided"""
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
    
    #replace existing object manager
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined'] 

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    service_type = models.CharField(
        max_length=5,
        choices=SERVICE_TYPE_CHOICES,
        default='type1'
    )
    description = models.TextField()
    files = models.FileField(
        upload_to='service_docs/',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='pending'
    )
    note = models.TextField(
        blank=True,
        help_text="Staff comments or updates about the request"
    )
    ser_req_no= models.CharField(
        unique=True,
        max_length=6
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ser_req_no:
            self.ser_req_no = str(uuid.uuid4().int)[:6]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_service_type_display()} -{self.status}  {self.created_at}"


