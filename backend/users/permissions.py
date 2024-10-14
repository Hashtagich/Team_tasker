from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Group, CustomUser


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            raise PermissionDenied("Данный функционал доступен только пользователям с ролью Администратор.")
        else:
            return True


class IsNotBlocked(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.is_blocked:
            raise PermissionDenied("Ваша учётная запись заблокирована.")
        else:
            return True


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        user = request.user

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise PermissionDenied("Группа не найдена.")

        if group.moderators.filter(id=user.id).exists() or user.is_staff:
            return True
        else:
            raise PermissionDenied("Редактировать группу могу администраторы и её модераторы.")


class IsAuthorModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        try:
            task = view.get_object()
            author = task.author
        except Exception as e:
            raise PermissionDenied("Не удалось получить автора задачи.")

        if user.is_staff or user.id == author.id:
            return True

        user_groups = user.groups.all()

        if user_groups.filter(moderators=user).exists():
            return True
        else:
            raise PermissionDenied("Вы должны быть модератором группы автора.")
