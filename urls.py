from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse 
from rest_framework.routers import DefaultRouter
 # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),  # adjust this if your app name is different
    path('', lambda request: HttpResponse("<h1>🎉 Django API is working!</h1><p>Try /api/signup/</p>")),
]
router = DefaultRouter() 