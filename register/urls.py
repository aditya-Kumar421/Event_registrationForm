from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ad/', include('form.urls')),
    # path('admin/defender', include('defender.urls')),
]