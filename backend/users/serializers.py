from rest_framework import serializers
from .models import CustomUser, School
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name')
        read_only_fields = ('id', 'name') # For read-only display in user profile

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model used to return user data (e.g., profile).
    """
    school = SchoolSerializer(read_only=True) # Nested School data
    
    class Meta:
        model = CustomUser
        # Exclude sensitive fields like 'password' and permissions fields
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role', 'school', 
            'is_active', 'is_staff', 'date_joined'
        )
        read_only_fields = ('id', 'email', 'role', 'school', 'is_active', 'is_staff', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for handling new user registration.
    Requires email, first_name, last_name, password, and password_confirm.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'role', 'password', 'password_confirm')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        """
        Check that the two password fields match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Password fields didn't match."})
        
        # Remove password_confirm before returning validated data
        data.pop('password_confirm')
        return data

    def create(self, validated_data):
        """
        Create the user using the custom manager's create_user method.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data.get('role', CustomUser.Role.STUDENT),
        )
        return user