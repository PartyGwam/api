from rest_framework import permissions


class IsAuthenticatedOrRegistering(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user and request.user.is_authenticated


class IsMyself(permissions.IsAuthenticated):
    message = '현재 로그인 되어있는 유저가 아닙니다.'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return request.user == obj
