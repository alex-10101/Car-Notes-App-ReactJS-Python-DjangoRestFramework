from django.conf import settings
from django.urls import path, re_path

# from .views_OLD_with_recaptcha import ActivateAccountView, LogoutAllDevicesView, RegisterWithSendingEmailView, GetCSRFCookie, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView, RequestChangeForgottenPasswordView, ConfirmChangeForgottenPasswordView
from .views import ActivateAccountView, LogoutAllDevicesView, RegisterWithSendingEmailView, GetCSRFCookie, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView, RequestChangeForgottenPasswordView, ConfirmChangeForgottenPasswordView

from django.views.static import serve

urlpatterns = [
    path("csrf_cookie/", GetCSRFCookie.as_view(), name="csrf_cookie"),
    path("is_authenticated/", CheckAuthenticatedView.as_view(), name="is_authenticated"),
    # path("register/", RegisterView.as_view(), name="register"),
    path("register/", RegisterWithSendingEmailView.as_view(), name="register"),
    path("activate_account/<str:uidb64>/<str:token>/", ActivateAccountView.as_view(), name="activate_account"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout_all/", LogoutAllDevicesView.as_view(), name="logout"),
    # path("change_known_password/", ChangeKnownPasswordView.as_view(), name="change_known_password"),
    path("request_change_known_password/", RequestChangeForgottenPasswordView.as_view(), name="request_change_known_password"),
    path("confirm_change_known_password/<str:uidb64>/<str:token>/", ConfirmChangeForgottenPasswordView.as_view(), name="confirm_change_known_password"),
    path("delete_account/", DeleteAccountView.as_view(), name="delete_account"),
]

