from rest_framework import permissions


class UserAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return request.user == obj
