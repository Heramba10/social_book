from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UploadedFileSerializer
from rest_framework.response import Response
from .forms import UploadedFileForm
from .models import UploadedFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse

from .forms import CreateUserForm


User = get_user_model()

# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user  # Assign the currently logged-in user
            uploaded_file.save()
            messages.success(request, "Book uploaded successfully!")
            return redirect("index")  # Redirect to the same page after successful upload
        else:
            messages.error(request, "There was an error with your upload. Please try again.")
    else:
        form = UploadedFileForm()

    # Fetch uploaded files to display on the page
    uploaded_files = UploadedFile.objects.filter(uploaded_by=request.user)

    context = {
        "form": form,
        "uploaded_files": uploaded_files,
    }
    return render(request, "index.html", context)
   

@csrf_protect
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request,'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('userlogin')
    
    context = { 'form':form}
    return render(request,'register.html',context)
    #return HttpResponse("this is about page")

@csrf_protect
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        
        if user is not None:
            login(request, user)
                        # Generate JWT token
            serializer = TokenObtainPairSerializer(data={"email": email, "password": password})
            if serializer.is_valid():
                
                tokens = serializer.validated_data
                access_token = tokens['access']
                refresh_token = tokens['refresh']
                
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                
                
                response = redirect('index')
                response.set_cookie('access_token', access_token)  # Store token in cookie if needed
                response.set_cookie('refresh_token', refresh_token) 
                
                return response
                
            else:
                messages.error(request, 'Token generation failed')
                return redirect('login')  # Redirect back to login if token generation fails

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('userLogin')  # Redirect back to login on failed authentication

            
            
            
       
           

    return render(request,'login.html')
    #return HttpResponse("this is about page")
    
    
def userLogout(request):
    logout(request)
    return redirect('userlogin')    
    
    
    
def authors_sellers(request):
    # Query users who have opted for public_visibility
    visible_users = User.objects.filter(public_visibility=True)
    
    context = {
        'visible_users': visible_users  # Correct the context name
    }
    return render(request, 'authors_sellers.html', context)


class UserFilesAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Fetch uploaded files by the authenticated user
        uploaded_files = UploadedFile.objects.filter(uploaded_by=request.user)
        
        # Serialize the file data
        serializer = UploadedFileSerializer(uploaded_files, many=True)
        
        # Return the serialized data as a JSON response
        return Response({"files": serializer.data})

"""@login_required
def upload_books(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user  # Assign current user to the uploaded file
            uploaded_file.save()
            return redirect('uploaded_files')  # Redirect to the uploaded files section after successful upload
    else:
        form = UploadedFileForm()

    return render(request, 'upload_books.html', {'form': form})


@login_required
def uploaded_files(request):
    # Fetch files uploaded by the user
    user_files = UploadedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'uploaded_files.html', {'user_files': user_files})"""
    
    
@login_required
def my_books(request):
    # Check if the user has uploaded any files
    uploaded_files = UploadedFile.objects.filter(uploaded_by=request.user)
    
    if uploaded_files.exists():
        # Show the user's uploaded files in "My Books" dashboard
        context = {'uploaded_files': uploaded_files}
        return render(request, 'my_books.html', context)
    else:
        # If no files, redirect to the upload page
        return redirect('index')  # Redirect to the upload section
    
    
    
  