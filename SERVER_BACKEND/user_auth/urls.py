from django.urls import path
from .views import RegisterView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView, ChangePasswordView

urlpatterns = [
    path("csrf_cookie", GetCSRFToken.as_view(), name="csrf_cookie"),
    path("is_authenticated", CheckAuthenticatedView.as_view(), name="is_authenticated"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("change_password", ChangePasswordView.as_view(), name="change_password"),
    path("delete_account", DeleteAccountView.as_view(), name="delete_account"),
]
