from django.contrib import admin
from .models import CustomUser
from .models import UploadedFile# Replace 'CustomUser' with the name of your custom user model

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']  # Adjust fields as necessary

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','cost','year_of_publication', 'uploaded_by']
   