# We are overriding the django authentication system, to allow users to login using their username, ignoring case sensitivity
# It was created with the help Vitor Freitas' article, link below:
# https://simpleisbetterthancomplex.com/tutorial/2017/02/06/how-to-implement-case-insensitive-username.html

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = f'{UserModel.USERNAME_FIELD}__iexact'
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
