from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'address' , 'phone_number', 'util_acc_no', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
