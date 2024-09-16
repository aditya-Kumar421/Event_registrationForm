from .serializers import RegistrationSerializer, EmailSerializer
from .models import Registration

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.exceptions import ValidationError

import requests

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError



class RegistrationList(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        
        def validate_phone_digits(value):
            value_str = str(value)
            if len(value_str) != 10:
                raise ValidationError("Contact number must have 10 digits.")
        
        def validate_student_digits(value):
            value_str = str(value)
            if not value_str.startswith('23'):
                raise ValidationError("Student number should start with '23'.")
            
        def validate_email(email):
            pattern = r'^([a-zA-Z]+)\+(\d+)@akgec\.ac\.in$'
            
            match = re.match(pattern, email)
            if not match:
                raise ValidationError('Email must be in the format string+studentnumber@akgec.ac.in')

            string_part, student_number = match.groups()
            if not student_number.isdigit():
                raise ValidationError('The student number must be numeric.')

        # Validate phone number and student number
        phone_number = request.data.get('phone_number', '')
        student_no = request.data.get('student_no', '')


        # Email validation
        email = request.data.get('email', '')
        if not email.endswith('@akgec.ac.in'):
            return Response({'error': 'Only college email id is allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_phone_digits(phone_number)
            validate_student_digits(student_no)
            validate_email(email)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

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
            subject = "SPOCC'24 Registration Confirmation 🚀 Event Details Inside!"
            email_from = settings.EMAIL_HOST_USER
            email_data = serializer.validated_data.get('email')
            recipient_list = [email_data]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return Response({'success': True, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response({'error': "reCAPTCHA verification failed"}, status=400)

class RegistrationView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        all_Questions = Registration.objects.order_by("-student_no")
        serializer = RegistrationSerializer(all_Questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisteredEmail(APIView):
    def get(self, request):
        emails = Registration.objects.all().values_list('email', flat=True)
        return Response(emails, status=status.HTTP_200_OK)

class RegistrationUpdateDeleteView(APIView):

    def get(self, request, student_no):
        try:
            raw_student = Registration.objects.get(student_no=student_no)
        except Registration.DoesNotExist:
            return Response({"Student not found"})
        serializer = RegistrationSerializer(raw_student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, student_no):
        try:
            stu = Registration.objects.get(student_no=student_no)
        except Registration.DoesNotExist:
            return Response({"Student not found"})
        serializer = RegistrationSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg: Student data Updated successfully!"})
        return Response(serializer.errors)

    def delete(self, request, student_no):
        try:
            stu = Registration.objects.get(student_no=student_no)
        except Registration.DoesNotExist:
            return Response({"Student not found"})
        stu.delete()
        return Response({"Student detail deleted successfully!"})


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            emails = serializer.validated_data['emails']
            email_from = settings.EMAIL_HOST_USER
            subject = " Confirmation Nimbus Event Payment"
            html_template = 'register_email.html'
            email_html_message = render_to_string(html_template)
            email_message = EmailMessage(subject, email_html_message, email_from, emails)
            email_message.content_subtype = "html" 
            email_message.send()
            
            return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)