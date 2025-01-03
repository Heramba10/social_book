from django.contrib import admin
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.userlogin, name="userlogin"),
    path('index',views.index, name="index"),
    path('register',views.register, name="register"),
    path('authors_sellers',views.authors_sellers, name="authors_sellers"),
     

    

]
