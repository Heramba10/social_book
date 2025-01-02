from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
    #return HttpResponse("this is about page")

def register(request):
    return render(request,'register.html')
    #return HttpResponse("this is about page")

def login(request):
    return render(request,'login.html')
    #return HttpResponse("this is about page")    