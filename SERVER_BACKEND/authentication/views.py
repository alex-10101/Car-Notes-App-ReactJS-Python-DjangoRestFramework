from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from .serlalizers import UserSerializer, RegisterSerializer, LoginSerializer, DeleteAccountSerializer, ChangePasswordSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import status
from django.middleware.csrf import rotate_token
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.utils import timezone

User = get_user_model()

# Create your views here.

class GetCSRFCookie(APIView):
    """View to get a CSRF cookie"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        When the client makes a page refresh, a request should be made to this endpoint to get a new csrf cookie.
        """ 
        rotate_token(request)
        return Response(status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name="dispatch") 
class CheckAuthenticatedView(APIView):
    """
    View to check if the current user is authenticated or not.
    When the client makes a page refresh, a request should be made to this endpoint to see if the user is authenticated.
    """

    def post(self, request):
        """Method which runs when the user submits a POST request to check if the current user is authenticated or not"""
        if bool(request.user and request.user.is_authenticated):
            user = UserSerializer(self.request.user)
            return Response({"user": user.data}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_protect, name="dispatch") 
class RegisterView(APIView):
    """View to register a new user with email, username, password and password confirmation."""
    permission_classes=(permissions.AllowAny,)

    def post(self, request):
        """Method which runs when the user submits a POST request to register a new user with username and password"""
    
        # extract email, username, password, confirmPassword from the data passed with the request (the request body)
        data = {
            "username": request.data["username"],
            "email": request.data["email"],
            "password": request.data["password"],
            "confirm_password": request.data["confirmPassword"],
            "captcha_value": request.data["captchaValue"]
        }

        serializer=RegisterSerializer(data=data)

        if serializer.is_valid():
            email=serializer.data["email"]
            password=serializer.data["password"]

            User.objects.create_user(email=email, username=serializer.data["username"], password=password)
            return Response(status=status.HTTP_201_CREATED)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


@method_decorator(csrf_protect, name="dispatch") 
class LoginView(APIView):
    """View to log in a user with username and password"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Method which runs when the user submits a POST request to log in."""
        data={
            "email": request.data["email"],
            "password": request.data["password"],
            "captcha_value": request.data["captchaValue"]
        }

        context={"request": request}

        serializer=LoginSerializer(data=data, context=context)

        if serializer.is_valid():

            email=serializer.data["email"]
            password=serializer.data["password"]
            
            # authenticate with email and password (Django's default authentication is with username and password)
            user = auth.authenticate(username=email, password=password)

            if user is None: 
                return Response({"detail": "Wrong username or password or inactive user."}, status=status.HTTP_400_BAD_REQUEST)
            
            auth.login(request, user)
            user = UserSerializer(self.request.user)
            return Response({"user": user.data}, status=status.HTTP_204_NO_CONTENT)
        
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
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(request.user.id):
                session.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteAccountView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def delete(self, request):
        """Delete the account of the current user (the user making the request)"""
        data = {
            "password": request.data["password"],
        }

        context={"request": request}

        serializer=DeleteAccountSerializer(data=data, context=context)

        if serializer.is_valid():
            user=request.user
            User.objects.filter(id=user.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def put(self, request):
        """Change the password of the current user (the user making the request)"""
        
        data = {
            "old_password": request.data["oldPassword"],
            "new_password": request.data["newPassword"],
            "new_password_confirm": request.data["newPasswordConfirm"],
        }

        context={'request': request}

        serializer=ChangePasswordSerializer(data=data, context=context)

        if serializer.is_valid():
            user=request.user
            user.set_password(data["new_password"])
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





