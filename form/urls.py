from django.urls import path
from .views import RegistrationList

urlpatterns = [
    path('register/', RegistrationList.as_view(), name='registration'),
]
