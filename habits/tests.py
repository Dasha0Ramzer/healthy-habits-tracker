from datetime import time

from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit


class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", password=make_password("StrongPass123")
        )
        self.other = User.objects.create(
            email="other@example.com", password=make_password("StrongPass123")
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Зарядка",
            duration=60,
        )

    def test_create(self):
        response = self.client.post(
            "/habits/create/",
            {
                "place": "Парк",
                "time": "07:00",
                "action": "Бег",
                "duration": 60,
                "frequency_days": 1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], self.user.id)

    def test_reward_and_related(self):
        response = self.client.post(
            "/habits/create/",
            {
                "place": "Парк",
                "time": "07:00",
                "action": "Бег",
                "duration": 60,
                "reward": "Конфета",
                "related_habit": self.habit.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_pleasant_no_reward(self):
        response = self.client.post(
            "/habits/create/",
            {
                "place": "Парк",
                "time": "07:00",
                "action": "Бег",
                "duration": 60,
                "is_pleasant": True,
                "reward": "Конфета",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_related_must_be_pleasant(self):
        response = self.client.post(
            "/habits/create/",
            {
                "place": "Парк",
                "time": "07:00",
                "action": "Бег",
                "duration": 60,
                "related_habit": self.habit.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_list_own_and_public(self):
        public_habit = Habit.objects.create(
            user=self.other,
            place="Дом",
            time=time(9, 0),
            action="Медитация",
            duration=60,
            is_public=True,
        )
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, 200)
        ids = [h["id"] for h in response.data["results"]]
        self.assertIn(self.habit.id, ids)
        self.assertIn(public_habit.id, ids)

    def test_private_other_forbidden(self):
        habit = Habit.objects.create(
            user=self.other,
            place="Дом",
            time=time(9, 0),
            action="Секрет",
            duration=60,
        )
        response = self.client.get(f"/habits/{habit.id}/")
        self.assertEqual(response.status_code, 403)

    def test_public_other_ok(self):
        habit = Habit.objects.create(
            user=self.other,
            place="Дом",
            time=time(9, 0),
            action="Медитация",
            duration=60,
            is_public=True,
        )
        response = self.client.get(f"/habits/{habit.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_other_forbidden(self):
        habit = Habit.objects.create(
            user=self.other,
            place="Дом",
            time=time(9, 0),
            action="Бег",
            duration=60,
        )
        response = self.client.patch(
            f"/habits/{habit.id}/update/",
            {"action": "Хак"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_other_forbidden(self):
        habit = Habit.objects.create(
            user=self.other,
            place="Дом",
            time=time(9, 0),
            action="Бег",
            duration=60,
        )
        response = self.client.delete(f"/habits/{habit.id}/delete/")
        self.assertEqual(response.status_code, 403)

    def test_pagination(self):
        response = self.client.get("/habits/")
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
