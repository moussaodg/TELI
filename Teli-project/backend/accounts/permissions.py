from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role is not None
            and request.user.role.authorisation == 'superadmin'
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role is not None
            and request.user.role.authorisation in ('manager', 'superadmin')
        )
