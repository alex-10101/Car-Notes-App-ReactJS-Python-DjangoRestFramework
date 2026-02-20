import os
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response

from utils.frontendURL import FRONTEND_URL
from .serlalizers import RecoverPasswordSerializer, ResetPasswordSerializer, GetUserSerializer, RegisterSerializer, LoginSerializer, DeleteAccountSerializer, ChangePasswordSerializer
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from django.middleware.csrf import rotate_token
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.signing import BadSignature
# from utils.generateAccountActivationToken import account_activation_token

# from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from importlib import import_module
from django.conf import settings


User = get_user_model()

# generates a one time-token for activating accounts and for resetting passwords.
generated_token = PasswordResetTokenGenerator()

# Create your views here.

class GetCSRFCookie(APIView):
    """View to get a CSRF cookie"""
    permission_classes = (permissions.AllowAny,)

    # def get(self, request):
    #     """
    #     When the client makes a page refresh, a request should be made to this endpoint to get a new csrf cookie.
    #     """
    #     rotate_token(request)
    #     return Response(status=status.HTTP_200_OK)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        """
        When the client app mounts and there is no CSRF cookie, a request should be made to this endpoint to get a new csrf cookie.
        """
        return Response(status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    """
    View to check if the current user is authenticated or not.
    When the client makes a page refresh, a request should be made to this endpoint to see if the user is authenticated.
    """

    def get(self, request):
        """Method which runs when the user submits a GET request to check if the current user is authenticated or not"""
        if bool(request.user and request.user.is_authenticated):
            user = GetUserSerializer(self.request.user)
            return Response({"user": user.data}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


# @method_decorator(csrf_protect, name="dispatch")
# class RegisterView(APIView):
#     """View to register a new user with email, username, password and password confirmation."""
#     permission_classes=(permissions.AllowAny,)

#     def post(self, request):
#         """Method which runs when the user submits a POST request to register a new user with username and password"""

#         # extract email, username, password, confirmPassword from the data passed with the request (the request body)
#         data = {
#             "username": request.data["username"],
#             "email": request.data["email"],
#             "password": request.data["password"],
#             "confirm_password": request.data["confirmPassword"],
#             "captcha_value": request.data["captchaValue"]
#         }

#         serializer=RegisterSerializer(data=data)

#         if serializer.is_valid():
#             email=serializer.data["email"]
#             password=serializer.data["password"]

#             User.objects.create_user(email=email, username=serializer.data["username"], password=password)
#             return Response(status=status.HTTP_201_CREATED)

#         return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class RegisterWithSendingEmailView(APIView):
    """View to register a new user with email, username, password and password confirmation."""
    permission_classes=(permissions.AllowAny,)

    def __send_account_activation_email(self, user):
        """
        Private method, which generates uid and a token and create the activation link using these values. 
        Then an email is sent to the user with this activation link.
        """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # token = account_activation_token.make_token(user)
        token = generated_token.make_token(user)

        # current_site = get_current_site(request)
        # activation_link = f"{current_site}/activate/{uid}/{token}/" # if we also use Django for the frontend
        activation_link = f"{FRONTEND_URL}/activate/{uid}/{token}/"

        # send_mail(
        #     subject="Activate Your Account",
        #     message=f"Dear {user.username}, activate your account by clicking here: {activation_link}. If you want to receive a new link, register again with the same email but with a different username. Your data (id, username, password), will not change.",            
        #     recipient_list=[user.email],
        #     from_email=os.environ["EMAIL_FROM"]
        # )

        mail_subject = 'Activate your user account.'
        message = render_to_string(template_name="authentication/template_activate_account.html", context={
            'username': user.username,
            'activation_link': activation_link,
        })

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html" # to render html tags in the template. Without this, the html tags will be shown as strings. 

        email.send()

    def post(self, request):
        """Method which runs when the user submits a POST request to register a new user with username and password"""

        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            email=validated_data["email"]
            password=validated_data["password"]
            username=validated_data["username"]

            # Check if user with given email already exists.
            # If yes, send an email to the user 
            # without changing the other user information (id, username, password).
            # There should be only one user with that email address.
            try:
                user_with_email = User.objects.get(email=email)

                if user_with_email:
                    self.__send_account_activation_email(user_with_email)
                    return Response(f"Please check your email to activate your account.", status=status.HTTP_201_CREATED)
        
            except User.DoesNotExist:
                user_with_email=None


            # Create the user with the given email, username, password.
            user = User.objects.create_user(email=email, username=username, password=password)

            # Make user inactive. If the user is not active, he/she cannot log in.
            # The user will be set to active after he/she activates his/her account.
            user.is_active = False
            user.save()

            self.__send_account_activation_email(user)

            return Response(f"Please check your email to activate your account.", status=status.HTTP_201_CREATED)

        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class ActivateAccountView(APIView):
    def post(self, request, uidb64, token):
        """
        First, decode the "uidb64" and "token" given in an activation email link.
        Then, check whether the user exists in our database with a decoded primary key.
        If the user exists, we are checking whether the token is not expired yet.
        If not, we set the user as active and redirect it back to the login page.
        """

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BadSignature, User.DoesNotExist):
            user = None

        # if user is not None and account_activation_token.check_token(user, token):
        #     user.is_active = True
        #     user.save()
        #     return Response('Account activated successfully!', status=status.HTTP_200_OK)

        if user is not None and generated_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Account activated successfully!', status=status.HTTP_200_OK)


        return Response({"detail": "Account Activation Failed."}, status=status.HTTP_400_BAD_REQUEST)    


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    """View to log in a user with username and password"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Method which runs when the user submits a POST request to log in."""
        context={"request": request}

        serializer=LoginSerializer(data=request.data, context=context)

        if serializer.is_valid():

            email=serializer.validated_data["email"]
            password=serializer.validated_data["password"]

            # authenticate with email and password (Django's default authentication is with username and password)
            user = auth.authenticate(username=email, password=password)

            # Some possible reasons for error: wrong username or password or the user is inactive.
            if user is None:
                return Response({"detail": "Could not log in."}, status=status.HTTP_400_BAD_REQUEST)

            auth.login(request, user)
            user = GetUserSerializer(self.request.user)
            return Response({"user": user.data}, status=status.HTTP_200_OK)

        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """View to log a user out."""
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        """Method which runs when the user submits a POST request to log out."""
        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAllDevicesView(APIView):
    """View to log a user out of all devices."""
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        """Method which runs when the user submits a POST request to log out."""

        # Get all active sessions
        sessions = Session.objects.filter(expire_date__gte=timezone.now())

        # Loop through sessions and delete those for the current user
        for session in sessions:

            SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
            s = SessionStore(session_key=session.session_key)

            session_data = session.get_decoded()

            if session_data.get('_auth_user_id') == str(request.user.id):
                # this deletes from the cache
                s.delete()
                # this deletes from the database (but not also from the cache)
                session.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteAccountView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def delete(self, request):
        """Delete the account of the current user (the user making the request)"""
        context={"request": request}

        serializer=DeleteAccountSerializer(data=request.data, context=context)

        if serializer.is_valid():
            user=request.user
            User.objects.filter(id=user.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# class ChangeKnownPasswordView(APIView):
#     permission_classes=[permissions.IsAuthenticated]

#     def put(self, request):
#         """Change the password of the current user (the user making the request)"""

#         data = {
#             "old_password": request.data["oldPassword"],
#             "new_password": request.data["newPassword"],
#             "new_password_confirm": request.data["newPasswordConfirm"],
#         }

#         context={'request': request}

#         serializer=ChangePasswordSerializer(data=data, context=context)

#         if serializer.is_valid():
#             user=request.user
#             user.set_password(serializer.data["new_password"])
#             user.save()

#             return Response(status=status.HTTP_204_NO_CONTENT)

#         return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class RequestChangeForgottenPasswordView(APIView):

    def __send_recover_password_email(self, user):
        """
        Private method, which, for an existing user, generates uid and a token and create the activation link using these values. 
        Then an email is sent to the user with this activation link.
        """

        # if there is no user, send en empty email to reduce timing difference between users with email and users without email
        if user == None:
            email = EmailMessage(subject="...", body="...", to=["non-existing-email@gmail.com"])
            email.content_subtype = "html" # to render html tags in the template. Without this, the html tags will be shown as strings. 
            email.send()
            return

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # token = account_activation_token.make_token(user)
        token = generated_token.make_token(user)

        # current_site = get_current_site(request)
        # activation_link = f"{current_site}/confirmChangeForgottenPassword/{uid}/{token}/" # if we also use Django for the frontend
        activation_link = f"{FRONTEND_URL}/confirmChangeForgottenPassword/{uid}/{token}/"

        mail_subject = 'Password Reset request.'
        message = render_to_string(template_name="authentication/template_recover_password.html", context={
            'username': user.username,
            'activation_link': activation_link,
        })

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html" # to render html tags in the template. Without this, the html tags will be shown as strings. 

        email.send()

    def post(self, request):
        serializer = RecoverPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email=serializer.data["email"]

            associated_user = None
            try:
                associated_user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            self.__send_recover_password_email(user=associated_user)

            return Response(f"Please check your email to recover your password.", status=status.HTTP_200_OK)

        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class ConfirmChangeForgottenPasswordView(APIView):

    def put(self, request, uidb64, token):
        """
        First, extract the data passed with the request and pass them to the serializer.
        Then, decode the "uidb64" and "token" given in an reset password email link.
        Then, check whether the user exists in our database with a decoded primary key.
        If the user exists, we are checking whether the token is not expired yet.
        If not, we set the user as active and redirect it back to the login page.
        """

        context={'request': request}

        serializer=ResetPasswordSerializer(data=request.data, context=context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BadSignature, User.DoesNotExist):
            user = None

        if user is not None and generated_token.check_token(user, token):

            if serializer.is_valid():
                user.set_password(serializer.validated_data["newPassword"])
                user.save()
                return Response('Password reset was successful!', status=status.HTTP_200_OK)
            
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Password reset failed."}, status=status.HTTP_400_BAD_REQUEST)



