from rest_framework import permissions


class IsAuthor(permissions.IsAuthenticated):
    message = '댓글 작성자만 수정 및 삭제가 가능합니다.'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return request.user.profile == obj.author
