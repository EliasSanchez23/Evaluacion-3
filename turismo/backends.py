# turismo/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(correo=username)
        except UserModel.DoesNotExist:
            logger.debug(f'User with email {username} does not exist')
            return None
        
        if user.check_password(password):
            logger.debug(f'Password for user {username} is correct')
            return user
        else:
            logger.debug(f'Password for user {username} is incorrect')
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

