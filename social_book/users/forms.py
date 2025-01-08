from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UploadedFile
from .models import CustomUser

User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom user model
        fields = ['username', 'email', 'password1', 'password2']



class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'visibility', 'cost', 'year_of_publication', 'uploaded_file'] 
        
        

class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birth_year', 'address', 'public_visibility']
        widgets = {
            'public_visibility': forms.CheckboxInput(),
        }
               
    def __init__(self, *args, **kwargs):
        super(CustomUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True            