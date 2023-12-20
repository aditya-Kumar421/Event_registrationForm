from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('registrationPortalDatabase/', admin.site.urls),
    path('ad/', include('form.urls')),
    path('registrationPortalDatabase/defender', include('defender.urls')),
]