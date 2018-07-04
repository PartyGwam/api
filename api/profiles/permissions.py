from rest_framework.permissions import IsAuthenticated


class ProfileAPIPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj == request.user.profile
