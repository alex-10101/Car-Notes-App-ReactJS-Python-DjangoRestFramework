from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, DeleteAccountSerializer, ChangePasswordSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import status

# Create your views here.

@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    """View to get a CSRF token (CSRF token is sent to the client, for example: a React app)"""
    permission_classes = (permissions.AllowAny,)


    def post(self, request):
        return Response(status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name="dispatch") 
class CheckAuthenticatedView(APIView):
    """
    View to check if the current user is authenticated or not.
    When the client makes a page refresh, a request should be made to this endpoint to see if the user is authenticated.
    """

    def post(self, request):
        """Method which runs when the user submits a POST request to check if the current user is authenticated or not"""
        try:
            if bool(request.user and request.user.is_authenticated):
                user = UserSerializer(self.request.user)
                return Response({"user": user.data}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name="dispatch") 
class RegisterView(APIView):
    """View to register a new user with email, username, password and password confirmation."""
    permission_classes=(permissions.AllowAny,)

    def post(self, request):
        """Method which runs when the user submits a POST request to register a new user with username and password"""
        
        try:
            # extract email, username, password, confirmPassword from the data passed with the request (the request body)
            data = {
                "username": request.data["username"],
                "email": request.data["email"],
                "password": request.data["password"],
                "confirm_password": request.data["confirmPassword"]
            }

            serializer=RegisterSerializer(data=data)

            if serializer.is_valid():
                email=serializer.data["email"]
                password=serializer.data["password"]

                User.objects.create_user(email=email, username=serializer.data["username"], password=password)
                return Response(status=status.HTTP_201_CREATED)
            
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name="dispatch") 
class LoginView(APIView):
    """View to log in a user with username and password"""

    permission_classes = (permissions.AllowAny,)
    # throttle_scope = "login"

    def post(self, request):
        """Method which runs when the user submits a POST request to log in."""
        try:
            data={
                "username": request.data["username"],
                "password": request.data["password"],
            }

            serializer=LoginSerializer(data=data)

            if serializer.is_valid():

                username=serializer.data["username"]
                password=serializer.data["password"]
                
                user = auth.authenticate(username=username, password=password)

                if user is None: 
                    return Response({"detail": "Wrong username or password or inactive user."}, status=status.HTTP_400_BAD_REQUEST)
                
                auth.login(request, user)
                user = UserSerializer(self.request.user)
                return Response({"user": user.data}, status=status.HTTP_204_NO_CONTENT)
            
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name="dispatch") 
class LogoutView(APIView):
    """View to log a user out."""
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        """Method which runs when the user submits a POST request to log out."""
        try:
            auth.logout(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_protect, name="dispatch")    
class DeleteAccountView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def delete(self, request):
        """Delete the account of the current user (the user making the request)"""
        try:
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
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChangePasswordView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    # throttle_scope = "login"

    def put(self, request):
        """Change the password of the current user (the user making the request)"""
        try: 
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
        except:
            return Response(
                {"detail": "Did not complete action, an unexpected error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)





