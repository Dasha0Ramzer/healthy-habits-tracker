# Healthy Habits Tracker

Django REST Framework проект для трекинга привычек.

## Технологии
- Python 3.14
- Django + DRF
- PostgreSQL
- Celery + django-celery-beat
- JWT-авторизация (SimpleJWT)
- Swagger (drf-yasg)

## Установка
1. `poetry install`
2. Настрой `.env` (SECRET_KEY, DB_*, CELERY_*, и т.д.)
3. `python manage.py migrate`
4. `python manage.py runserver`

## Запуск Celery
```bash
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
