from django.contrib.auth.backends import ModelBackend


class PGBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True
