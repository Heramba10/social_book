from django.contrib import admin
from django.urls import path,include
from users import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserFilesAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #path('api-auth/', include('rest_framework.urls')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('',views.userlogin, name="userlogin"),
    path('logout',views.userLogout, name="logout"),
    path('index',views.index, name="index"),
    path('register',views.register, name="register"),
    path('authors_sellers',views.authors_sellers, name="authors_sellers"),
    path('my_books/', views.my_books, name='my_books'), 
    path('api/my-files/', UserFilesAPI.as_view(), name='user-files-api')
 

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
