from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('my_api.urls')),  # Prefix API endpoints with /api/
]
