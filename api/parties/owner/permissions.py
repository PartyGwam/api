from rest_framework import permissions


class IsPartyOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return request.user.profile == obj.party_owner
