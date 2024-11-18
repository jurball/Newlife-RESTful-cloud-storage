from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest.serializers import RegistrationSerializer, AuthorizationSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():

            user_data = serializer.save()

            return Response({
                'success': True,
                'message': 'Success',
                'token': user_data['token']
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AuthorizationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthorizationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'message': 'Success',
                    'token': token.key
                }, status=status.HTTP_200_OK)

            return Response({
                'success': False,
                'message': 'login failed',
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = Token.auth

        if token:
            token.delete()
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'No token provided'
        }, status=status.HTTP_400_BAD_REQUEST)