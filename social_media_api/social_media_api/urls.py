# social_media_api/social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),              # Admin site
    path('api/accounts/', include('accounts.urls')),  # Accounts app routes
    path('api/', include('posts.urls')),             # Posts app routes
]
