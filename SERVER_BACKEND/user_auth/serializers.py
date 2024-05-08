from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from utils.sanitizeUserInput import sanitize_user_input

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields=["username", "email", "password", "confirm_password"]

    def validate_username(self, value):
        validate_username = UnicodeUsernameValidator()
        try:
            validate_username(value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages)
        return value

    def validate_email(self, value):
        validate_email = EmailValidator()
        try:
            validate_email(value)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages)
        return value  
        
    def validate(self, data):

        data=sanitize_user_input(data)

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # try to create the user with the given username and password            
        user = User.objects.create_user(email=data["email"], username=data["username"], password=data["password"])

        # validate the user's password. Delete the created user afterwards. User is creted in views.py
        try:
            validate_password(password=data["password"], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        finally:
            user.delete()

        return data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255)    
    password=serializers.CharField(max_length=255)    

    def validate(self, data):
        data=sanitize_user_input(data)

        try:
            user_with_given_username = User.objects.get(username = data["username"])
        except:
            raise serializers.ValidationError({"username": "Username does not exist. Go to register page."})
        if not user_with_given_username.check_password(raw_password=data["password"]):
            raise serializers.ValidationError({"password": "Wrong password."})
        return data
    
class DeleteAccountSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255)    

    def validate(self, data):
        data=sanitize_user_input(data)

        user=self.context["request"].user
        if not user.check_password(raw_password=data["password"]):
            raise serializers.ValidationError({"password": "Wrong password."})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(max_length=255)
    new_password=serializers.CharField(max_length=255)
    new_password_confirm=serializers.CharField(max_length=255)

    def validate(self, data):
        data=sanitize_user_input(data)

        user = self.context["request"].user

        if not user.check_password(raw_password=data["old_password"]):
            raise serializers.ValidationError({"password": "Wrong old password."})
                
        try:
            validate_password(password=data["new_password"], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError({"password": "New passwords do not match."})

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


