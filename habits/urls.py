from django.urls import path

from .views import (HabitCreateView, HabitDestroyView, HabitListView,
                    HabitRetrieveView, HabitUpdateView, PublicHabitListView)

urlpatterns = [
    path("", HabitListView.as_view(), name="habit_list"),
    path("public/", PublicHabitListView.as_view(), name="public_habit_list"),
    path("create/", HabitCreateView.as_view(), name="habit_create"),
    path("<int:pk>/", HabitRetrieveView.as_view(), name="habit_retrieve"),
    path("<int:pk>/update/", HabitUpdateView.as_view(), name="habit_update"),
    path("<int:pk>/delete/", HabitDestroyView.as_view(), name="habit_delete"),
]
