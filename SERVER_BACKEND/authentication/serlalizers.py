from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from utils.sanitizeUserInput import sanitize_user_input
import os
import requests

User = get_user_model()

class RecoverPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["email"]

        # override the default error messages:
        extra_kwargs = {
            "email": {
                "error_messages": {
                    'required': 'Email is required.', 
                    'null': 'Email is required.', 
                    'invalid': 'Email is invalid.', 
                    'blank': 'Email is required.', 
                    'max_length': 'Email is too long.', 
                    'min_length': 'Email is too short.'
                }
            },
        }

    def validate(self, data):
        data=sanitize_user_input(data)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    # override the default error messages of the "confirm_password" field:
    custom_confirm_password_errors = {
        "error_messages": {
            'required': 'Password confirmation is required.', 
            'null': 'Password confirmation is required.', 
            'invalid': 'Password confirmation is invalid.', 
            'blank': 'Password confirmation is required.', 
            'max_length': 'Password confirmation is too long.', 
            'min_length': 'Password confirmation is too short.'
        }
    }

    confirmPassword = serializers.CharField(error_messages=custom_confirm_password_errors["error_messages"])

    class Meta:
        model = User
        fields=["username", "email", "password", "confirmPassword"]

        # override the default error messages:
        extra_kwargs = {
            "username": {
                "error_messages": {
                    'required': 'Username is required.', 
                    'null': 'Username is required.', 
                    'invalid': 'Username is invalid.', 
                    'blank': 'Username is required.', 
                    'max_length': 'Username is too long.', 
                    'min_length': 'Username is too short.'
                }
            },
            "email": {
                "error_messages": {
                    'required': 'Email is required.', 
                    'null': 'Email is required.', 
                    'invalid': 'Email is invalid.', 
                    'blank': 'Email is required.', 
                    'max_length': 'Email is too long.', 
                    'min_length': 'Email is too short.'
                }
            },
            "password": {
                "error_messages": {
                    'required': 'Password is required.', 
                    'null': 'Password is required.', 
                    'invalid': 'Password is invalid.', 
                    'blank': 'Password is required.', 
                    'max_length': 'Password is too long.', 
                    'min_length': 'Password is too short.'
                }
            }
        }

    # def __init__(self, *args, **kwargs):
    #     super(RegisterSerializer, self).__init__(*args, **kwargs)     

    #     # see the default error_messages for these fields (in models.py all these fields are CharFields of max_lenghth = 255 characters)

    #     # {'required': 'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['username'].error_messages)

    #     # {'required': 
    #     #  'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['password'].error_messages)

    #     # {'required': 'This field is required.', 
    #     #  'null': 'This field may not be null.', 
    #     #  'invalid': 'Not a valid string.', 
    #     #  'blank': 'This field may not be blank.', 
    #     #  'max_length': 'Ensure this field has no more than {max_length} characters.', 
    #     #  'min_length': 'Ensure this field has at least {min_length} characters.'}
    #     print(self.fields['confirm_password'].error_messages)

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

        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Create an unsaved user instance for password validation context
        temp_user = User(
            email=data["email"],
            username=data["username"],
        )

        try:
            validate_password(password=data["password"], user=temp_user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})

        return data


class LoginSerializer(serializers.Serializer):
    # override the default error messages of the email and password fields:
    custom_error_messages = {
        "email": {
            "error_messages": {
                'required': 'Email is required.', 
                'null': 'Email is required.', 
                'invalid': 'Email is invalid.', 
                'blank': 'Email is required.', 
                'max_length': 'Email is too long.', 
                'min_length': 'Email is too short.'
            }
        },
        "password": {
            "error_messages": {
                'required': 'Password is required.', 
                'null': 'Password is required.', 
                'invalid': 'Password is invalid.', 
                'blank': 'Password is required.', 
                'max_length': 'Password is too long.', 
                'min_length': 'Password is too short.'
            }
        }
    }

    email=serializers.CharField(error_messages = custom_error_messages["email"]["error_messages"])    
    password=serializers.CharField(error_messages = custom_error_messages["password"]["error_messages"])    

    def validate(self, data):
        data=sanitize_user_input(data)
        
        # try: 
        #     user_with_given_email = User.objects.get(email = data["email"])
        # except:
        #     raise serializers.ValidationError({"email": "Email does not exist. Go to register page."})
        # if not user_with_given_email.check_password(raw_password=data["password"]):
        #     raise serializers.ValidationError({"password": "Wrong password."})
        
        return data
    
class DeleteAccountSerializer(serializers.Serializer):
    # override the default error messages of the "password" field:
    custom_password_errors = {
        "error_messages": {
            'required': 'Password confirmation is required.', 
            'null': 'Password confirmation is required.', 
            'invalid': 'Password confirmation is invalid.', 
            'blank': 'Password confirmation is required.', 
            'max_length': 'Password confirmation is too long.', 
            'min_length': 'Password confirmation is too short.'
        }
    }

    password=serializers.CharField(error_messages = custom_password_errors["error_messages"])    

    def validate(self, data):
        data=sanitize_user_input(data)

        user=self.context["request"].user
        if not user.check_password(raw_password=data["password"]):
            raise serializers.ValidationError({"password": "Wrong password."})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    # override the default error messages of the "oldPassword", "newPassword", "newPasswordConfirm" fields:
    custom_password_errors = {
        "oldPassword": {
            "error_messages": {
                'required': 'Password is required.', 
                'null': 'Password is required.', 
                'invalid': 'Password is invalid.', 
                'blank': 'Password is required.', 
                'max_length': 'Password is too long.', 
                'min_length': 'Password is too short.'
            }
        },
        "newPassword": {
            "error_messages": {
                'required': 'New password is required.', 
                'null': 'New password is required.', 
                'invalid': 'New password is invalid.', 
                'blank': 'New password is required.', 
                'max_length': 'New password is too long.', 
                'min_length': 'New password is too short.'
            }
        },
        "newPasswordConfirm": {
            "error_messages": {
                'required': 'New password confirmation is required.', 
                'null': 'New password confirmation is required.', 
                'invalid': 'New password confirmation is invalid.', 
                'blank': 'New password confirmation is required.', 
                'max_length': 'New password confirmation is too long.', 
                'min_length': 'New password confirmation is too short.'
            }
        },

    }

    oldPassword=serializers.CharField(error_messages = custom_password_errors["oldPassword"]["error_messages"])
    newPassword=serializers.CharField(error_messages = custom_password_errors["newPassword"]["error_messages"])
    newPasswordConfirm=serializers.CharField(error_messages = custom_password_errors["newPasswordConfirm"]["error_messages"])

    def validate(self, data):
        data=sanitize_user_input(data)

        user = self.context["request"].user

        if not user.check_password(raw_password=data["oldPassword"]):
            raise serializers.ValidationError({"password": "Wrong old password."})
                
        try:
            validate_password(password=data["newPassword"], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        
        if data["newPassword"] != data["newPasswordConfirm"]:
            raise serializers.ValidationError({"password": "New passwords do not match."})

        return data
    
class ResetPasswordSerializer(serializers.Serializer):
    # override the default error messages of the "newPassword", "newPasswordConfirm" fields:
    custom_password_errors = {
        "newPassword": {
            "error_messages": {
                'required': 'New password is required.', 
                'null': 'New password is required.', 
                'invalid': 'New password is invalid.', 
                'blank': 'New password is required.', 
                'max_length': 'New password is too long.', 
                'min_length': 'New password is too short.'
            }
        },
        "newPasswordConfirm": {
            "error_messages": {
                'required': 'New password confirmation is required.', 
                'null': 'New password confirmation is required.', 
                'invalid': 'New password confirmation is invalid.', 
                'blank': 'New password confirmation is required.', 
                'max_length': 'New password confirmation is too long.', 
                'min_length': 'New password confirmation is too short.'
            }
        },

    }

    newPassword=serializers.CharField(error_messages = custom_password_errors["newPassword"]["error_messages"])
    newPasswordConfirm=serializers.CharField(error_messages = custom_password_errors["newPasswordConfirm"]["error_messages"])

    def validate(self, data):
        data=sanitize_user_input(data)

        user = self.context["request"].user
                
        try:
            validate_password(password=data["newPassword"], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        
        if data["newPassword"] != data["newPasswordConfirm"]:
            raise serializers.ValidationError({"password": "New passwords do not match."})

        return data



class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["email", "password", "is_active", "last_login"]

