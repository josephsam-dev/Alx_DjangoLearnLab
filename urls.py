# Run this from C:\Users\USER\Alx_DjangoLearnLab\api_project
$code = @'
# api_project/api_project/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # include the api app's urls.py
]
'@

Set-Content -Path .\api_project\urls.py -Value $code -Encoding UTF8
Write-Host "Wrote api_project\urls.py — now run: python manage.py runserver"
