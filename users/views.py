from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, BasePermission, IsAdminUser

from .serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserListView(ListAPIView):
    """Список пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCreateView(CreateAPIView):
    """Создание пользователя."""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="register_user",
        summary="Регистрация пользователя",
        description=("Создает нового пользователя."),
        request_body=UserCreateSerializer,
        responses={
            "201": openapi.Response(
                description="Пользователь создан", schema=UserSerializer
            ),
            "400": "Ошибки валидации",
        },
        examples={
            "application/json": {
                "email": "ivan@example.com",
                "password": "StrongPassword123",
            }
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRetrieveView(RetrieveAPIView):
    """Просмотр одного пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]


class UserUpdateView(UpdateAPIView):
    """Обновление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]


class UserDestroyView(DestroyAPIView):
    """Удаление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]
