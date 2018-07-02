from rest_framework import permissions
from apps.profiles.models import Profile


class IsCurrentUserEqualsPartyOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            party_owner = obj.party_owner
            current_user = request.user
            current_user_profile = Profile.objects.get(
                user__exact=current_user
            )

            has_permission = party_owner == current_user_profile
            if request.method == 'DELETE':
                return has_permission and obj.current_people < 2
            else:
                return has_permission

        return request.user and request.user.is_authenticated
