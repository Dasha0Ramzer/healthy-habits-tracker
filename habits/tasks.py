from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_reminder_about_habit():
    now = timezone.now()
    current_time = now.time()
    today = now.date()

    start_time = (
        timezone.datetime.combine(today, current_time) - timedelta(minutes=15)
    ).time()
    end_time = (
        timezone.datetime.combine(today, current_time) + timedelta(minutes=15)
    ).time()

    habits = Habit.objects.select_related("user").filter(
        time__gte=start_time,
        time__lte=end_time,
        user__tg_chat_id__isnull=False,
    )

    for habit in habits:
        if habit.last_reminded_at and now - habit.last_reminded_at < timedelta(
            days=habit.frequency_days
        ):
            continue
        message = (
            f"⏰ Напоминание: пора выполнить привычку!\n\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Вознаграждение: {habit.reward or 'нет'}\n"
        )

        send_telegram_message(habit.user.tg_chat_id, message)

        habit.last_reminded_at = now
        habit.save(update_fields=["last_reminded_at"])
