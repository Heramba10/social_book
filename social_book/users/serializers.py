# users/serializers.py

from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'title', 'description', 'visibility', 'cost', 'year_of_publication', 'uploaded_file']
