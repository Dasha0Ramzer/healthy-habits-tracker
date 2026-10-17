from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Только владелец может редактировать/удалять/просматривать свои привычки."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicOrOwner(BasePermission):
    """
    Просмотр — если привычка публичная ИЛИ пользователь — владелец.
    Изменение/удаление — только владелец.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return obj.is_public or obj.user == request.user
        return obj.user == request.user
