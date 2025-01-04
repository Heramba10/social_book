from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UploadedFileForm
from .models import UploadedFile

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Username or password is incorrect')
           

    return render(request,'login.html')
    #return HttpResponse("this is about page")
    
    
    
def authors_sellers(request):
    # Query users who have opted for public_visibility
    visible_users = User.objects.filter(public_visibility=True)
    
    context = {
        'visible_users': visible_users  # Correct the context name
    }
    return render(request, 'authors_sellers.html', context)




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