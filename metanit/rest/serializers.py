from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def password_validator(password):
    if len(password) < 3:
        raise ValidationError('Password must be at least 3 characters long')

    if not any(char.islower() for char in password):
        raise ValidationError('Password must contain at least one lowercase letter')

    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least one uppercase letter')

    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit')

    return password

def email_validator(email):
    if get_user_model().objects.filter(email=email).exists():
        raise ValidationError('Email already registered')
    return email




class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[email_validator]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[password_validator]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )

            token = Token.objects.create(user=user)
            return {
                'user': user,
                'token': token.key
            }
        except ValidationError as e:
            raise serializers.ValidationError({'message': str(e)})


class AuthorizationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)