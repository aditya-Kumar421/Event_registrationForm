from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('registrationPortalDatabase/', admin.site.urls),
    path('form/', include('form.urls')),
]