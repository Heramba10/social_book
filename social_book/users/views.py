from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import CreateUserForm


User = get_user_model()

# Create your views here.
def index(request):
    return render(request,'index.html')
    #return HttpResponse("this is about page")

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