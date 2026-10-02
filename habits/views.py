from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from .models import Habit
from .paginators import CustomPagination
from .permissions import IsOwner, IsPublicOrOwner
from .serializers import HabitSerializer


class HabitListView(ListAPIView):
    """Список: свои привычки + публичные чужие."""

    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_id="list_habits",
        summary="Список привычек",
        description=(
            "Возвращает список привычек текущего пользователя и все публичные привычки других пользователей. "
        ),
        responses={
            "200": openapi.Response(
                description="Список привычек", schema=HabitSerializer(many=True)
            ),
            "401": "Требуется авторизация",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user) | Habit.objects.filter(
            is_public=True
        )


class HabitCreateView(CreateAPIView):
    """Создание привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @swagger_auto_schema(
        operation_id="create_habit",
        summary="Создать привычку",
        description="Создаёт привычку. Пользователь подставляется автоматически из токена.",
        request_body=HabitSerializer,
        responses={
            "201": openapi.Response(description="Создано", schema=HabitSerializer),
            "400": "Ошибки валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveView(RetrieveAPIView):
    """Просмотр одной привычки: своей или публичной."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsPublicOrOwner]

    @swagger_auto_schema(
        operation_id="get_habit",
        summary="Получить привычку",
        description=(
            "Возвращает данные привычки. Доступна только если привычка принадлежит текущему пользователю "
            "ИЛИ если привычка помечена как публичная (is_public=True). В противном случае — 403 Forbidden."
        ),
        responses={
            "200": openapi.Response(
                description="Данные привычки", schema=HabitSerializer
            ),
            "403": "Нет доступа к приватной привычке (не владелец и не публичная)",
            "404": "Привычка не найдена",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HabitUpdateView(UpdateAPIView):
    """Обновление привычки — только владелец."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitDestroyView(DestroyAPIView):
    """Удаление привычки — только владелец."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class PublicHabitListView(ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
