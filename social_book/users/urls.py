from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('',views.login, name="login"),
    path('index',views.index, name="index"),
    path('register',views.register, name="register"),

    

]
