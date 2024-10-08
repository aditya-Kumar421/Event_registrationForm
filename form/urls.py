from django.urls import path
from .views import RegistrationList, RegistrationView, RegistrationUpdateDeleteView, RegisteredEmail, SendEmailView, SendSingleEmailView

urlpatterns = [
    path('register/', RegistrationList.as_view(), name='registration'),
    path('data/', RegistrationView.as_view(), name='registrationData'),
    path('email/', RegisteredEmail.as_view(), name='registrationEmail'),
    path('update/<int:student_no>/', RegistrationUpdateDeleteView.as_view(), name='registrationChange'),
    path('sendemail/', SendEmailView.as_view(), name='sendemail'),
    path('mailer/', SendSingleEmailView.as_view(), name='emailer'),
]
