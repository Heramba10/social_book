from django.contrib import admin
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.userlogin, name="userlogin"),
    path('index',views.index, name="index"),
    path('register',views.register, name="register"),
    path('authors_sellers',views.authors_sellers, name="authors_sellers")
 

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
