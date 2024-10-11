from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            raise PermissionDenied("Данный функционал доступен только пользователям с ролью Администратор.")
        return True


class IsNotBlocked(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.is_blocked:
            raise PermissionDenied("Ваша учётная запись заблокирована.")
        return True
