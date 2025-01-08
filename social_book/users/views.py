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
from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail 

from .forms import CustomUserProfileForm
from .forms import CreateUserForm


User = get_user_model()

# Create your views here.

#Index View
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
   



#Register View
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




#Login View
@csrf_protect
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Ensure OTP device is confirmed
            device, created = EmailDevice.objects.get_or_create(user=user)
            if created:
                device.confirmed = True
                device.save()
            
            # Generate OTP
            otp_challenge = device.generate_challenge()# This will send the OTP to the user's email
            
            print(f"OTP sent to {user.email}:{otp_challenge}")
            # Debugging print statement
            
            # Redirect to OTP verification page
            return redirect('verify_otp')  # Redirect to OTP verification page
            
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('userLogin')  # Redirect back to login on failed authentication
    
    return render(request, 'login.html')
    


#Verify OTP View
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')  # Get the OTP entered by the user
        
        try:
            # Fetch the device associated with the user
            device = EmailDevice.objects.get(user=request.user, confirmed=True)
            
            if device.verify_token(otp):  # OTP verification
                # OTP is valid, proceed with JWT token generation
                # Send login notification email to the user
                login(request, request.user)
                
                subject = "Login Notification"
                message = f"Hello {request.user.username},\n\nYou have successfully logged in to your Social-Book account."
                send_mail(subject, message, 'herambakoli10@gmail.com', [request.user.email])
                
                # Optionally, generate JWT tokens
                refresh = RefreshToken.for_user(request.user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Save tokens in session (or cookies)
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                
                # Optionally, set tokens in cookies
                response = redirect('index')  # Redirect to the homepage or dashboard
                response.set_cookie('access_token', access_token)
                response.set_cookie('refresh_token', refresh_token)

                return response  # Complete the login flow after OTP verification
                
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('verify_otp')  # Retry OTP verification
        
        except EmailDevice.DoesNotExist:
            messages.error(request, 'OTP device not found')
            return redirect('userLogin')  # Redirect to login if no OTP device exists for the user
    
    return render(request, 'verify_otp.html')





#Logout View    
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
    
    
@login_required
def profile_view(request):
    user = request.user  # Logged-in user instance
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, instance=user)  # Bind form to the logged-in user
        if form.is_valid():
            form.save()  # Save the updated data
            print("Data saved successfully!")  # Debug success
            return redirect('index')  # Redirect to the same page after updating
        else:
            print(form.errors) 
          
    else:
        form = CustomUserProfileForm(instance=user)  # Pre-fill the form with user data

    return render(request, 'profile.html', {'form': form})
    
    
  