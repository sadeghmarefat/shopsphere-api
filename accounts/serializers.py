from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    

    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password', 'password_confirm')
        
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def validate_password(self, value):
        user = User(
            email=self.initial_data.get('email',''),
            first_name=self.initial_data.get('first_name','')
        )
        try:
            django_validate_password(value, user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user