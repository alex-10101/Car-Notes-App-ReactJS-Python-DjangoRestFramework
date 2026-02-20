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

    custom_captcha_value_errors = {
        "error_messages": {
            'required': 'Invalid reCAPTCHA.',
            'null': 'Invalid reCAPTCHA.',
            'invalid': 'Invalid reCAPTCHA.',
            'blank': 'Invalid reCAPTCHA.',
            'max_length': 'Invalid reCAPTCHA.',
            'min_length': 'Invalid reCAPTCHA.'
        }
    }

    confirm_password = serializers.CharField(error_messages=custom_confirm_password_errors["error_messages"])
    captcha_value = serializers.CharField(error_messages=custom_captcha_value_errors["error_messages"])

    class Meta:
        model = User
        fields=["username", "email", "password", "confirm_password", "captcha_value"]
        # fields=["username", "email", "password", "confirm_password"]

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


    def validate_captcha_value(self, value):
        secret_key = os.environ['GOOGLE_RECAPTCHA_PRIVATE_KEY']
        data = {'secret': secret_key, 'response': value}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        response_json = response.json()
        if response_json["success"] == False:
            raise serializers.ValidationError("Invalid reCAPTCHA.")
        return value

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

        # validate the user's password. Delete the created user afterwards. User is creted in views_OLD_with_recaptcha.py
        try:
            validate_password(password=data["password"], user=user)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})
        finally:
            user.delete()

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

    custom_captcha_value_errors = {
        "error_messages": {
            'required': 'Invalid reCAPTCHA.', 
            'null': 'Invalid reCAPTCHA.', 
            'invalid': 'Invalid reCAPTCHA.', 
            'blank': 'Invalid reCAPTCHA.', 
            'max_length': 'Invalid reCAPTCHA.', 
            'min_length': 'Invalid reCAPTCHA.'
        }
    }

    email=serializers.CharField(error_messages = custom_error_messages["email"]["error_messages"])    
    password=serializers.CharField(error_messages = custom_error_messages["password"]["error_messages"])    
    captcha_value = serializers.CharField(error_messages=custom_captcha_value_errors["error_messages"])

    def validate_captcha_value(self, value):
        secret_key = os.environ['GOOGLE_RECAPTCHA_PRIVATE_KEY']
        data= {'secret': secret_key, 'response': value}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        response_json = response.json()
        if response_json["success"] == False:
            raise serializers.ValidationError("Invalid reCAPTCHA.")
        return value

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
    # override the default error messages of the "old_password", "new_password", "new_password_confirm" fields:
    custom_password_errors = {
        "old_password": {
            "error_messages": {
                'required': 'Password is required.', 
                'null': 'Password is required.', 
                'invalid': 'Password is invalid.', 
                'blank': 'Password is required.', 
                'max_length': 'Password is too long.', 
                'min_length': 'Password is too short.'
            }
        },
        "new_password": {
            "error_messages": {
                'required': 'New password is required.', 
                'null': 'New password is required.', 
                'invalid': 'New password is invalid.', 
                'blank': 'New password is required.', 
                'max_length': 'New password is too long.', 
                'min_length': 'New password is too short.'
            }
        },
        "new_password_confirm": {
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

    old_password=serializers.CharField(error_messages = custom_password_errors["old_password"]["error_messages"])
    new_password=serializers.CharField(error_messages = custom_password_errors["new_password"]["error_messages"])
    new_password_confirm=serializers.CharField(error_messages = custom_password_errors["new_password_confirm"]["error_messages"])

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
    
class ResetPasswordSerializer(serializers.Serializer):
    # override the default error messages of the ", "new_password", "new_password_confirm" fields:
    custom_password_errors = {
        "new_password": {
            "error_messages": {
                'required': 'New password is required.', 
                'null': 'New password is required.', 
                'invalid': 'New password is invalid.', 
                'blank': 'New password is required.', 
                'max_length': 'New password is too long.', 
                'min_length': 'New password is too short.'
            }
        },
        "new_password_confirm": {
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

    new_password=serializers.CharField(error_messages = custom_password_errors["new_password"]["error_messages"])
    new_password_confirm=serializers.CharField(error_messages = custom_password_errors["new_password_confirm"]["error_messages"])

    def validate(self, data):
        data=sanitize_user_input(data)

        user = self.context["request"].user
                
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
        exclude = ["email", "password", "is_active", "last_login"]

