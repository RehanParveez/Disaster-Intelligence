from django.contrib import admin
from accounts.models import User, Profile

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['email', 'phone', 'control', 'dob', 'is_admin', 'created_at', 'updated_at']
  
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'location']
