from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Class which overrides the authenticate method in the ModelBackend class,
    which allows the users only to authenticate with username and password.
    This class allows the regular user to authenticate with email and password.
    (login in Django Admin is still with username and password)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # The username argument in this method can represent the email of the user making the request.
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
            return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user