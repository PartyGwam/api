from rest_framework.permissions import IsAuthenticated


class PartyAPIPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            has_permission = obj.party_owner == request.user.profile

            if request.method == 'DELETE':
                return has_permission and obj.current_people < 2
            else:
                return has_permission

        return request.user and request.user.is_authenticated
