from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from models import UserProfile

class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if 'uuid' in kwargs:
            try:
                return UserProfile.objects.get(uuid=kwargs['uuid'])
            except Exception, e:
                pass
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserProfile.objects.get(Q(email=username)|Q(mobile=username),Q(is_disabled=0))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)