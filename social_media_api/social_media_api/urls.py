from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Posts (likes / unlikes)
    path('api/', include('posts.urls')),

    # Notifications
    path('api/', include('notifications.urls')),

    # Accounts (if you have it)
    path('api/accounts/', include('accounts.urls')),
]
