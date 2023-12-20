from .serializers import RegistrationSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests
from django.conf import settings

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

class RegistrationList(APIView):
    def post(self, request,*args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        captcha_token = request.data.get('captcha', '')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': captcha_token
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()
        if result['success']:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            name_value = serializer.validated_data.get('name')
            mydict = {'name': name_value}    
            html_template = 'register_email.html'
            html_message = render_to_string(html_template, context = mydict)
            subject = 'Aditya Kumar'
            email_from = settings.EMAIL_HOST_USER
            email_data = serializer.validated_data.get('email')
            recipient_list = [email_data]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return Response({'success': True, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response({'errors': "reCAPTCHA verification failed"}, status=400)
