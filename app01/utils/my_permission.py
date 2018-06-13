from rest_framework.permissions import AllowAny, BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # 返回True则不限制访问
        if request.user:
            return True
        return False

class Permission(object):
    permission_classes = [CustomPermission,]
