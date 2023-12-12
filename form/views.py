from .serializers import RegistrationSerializer

import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
            return Response({'success': True, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response({'error': "reCAPTCHA verification failed"}, status=400)

