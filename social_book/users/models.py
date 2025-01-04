from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
import os


class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None


# Validator for file extension (pdf, jpeg only)


def file_extension_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpeg', '.jpg']
    if ext not in valid_extensions:
        raise ValidationError('File format not supported. Please upload PDF or JPEG files.')




class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.BooleanField(default=True)  # For visibility (True/False)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_of_publication = models.PositiveIntegerField()
    uploaded_file = models.FileField(upload_to='uploaded_books/', validators=[file_extension_validator])  # Only pdf/jpeg files
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Relating to the user

    def __str__(self):
        return self.title

