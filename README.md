# Healthy Habits Tracker

Django REST Framework проект для трекинга привычек.

## Технологии
- Python 3.14, Django + DRF
- PostgreSQL, Redis
- Celery + django-celery-beat
- JWT-авторизация (SimpleJWT)
- Swagger (drf-yasg)

## Запуск через Docker

1. Склонируйте репозиторий и перейдите в папку проекта.
2. Создайте файл `.env` по образцу `.env.example` (или скопируйте шаблон ниже) и заполните своими значениями:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DATABASE_NAME=имя_базы_данных
DATABASE_USER=имя_пользователя
DATABASE_PASSWORD=ваш_пароль
DB_HOST=db
EMAIL_HOST_USER=ваш_адрес_электронной_почты
EMAIL_HOST_PASSWORD=ваш_пароль_приложения_для_яндекс_почты
STRIPE_API_KEY=ваш_ключ_stripe
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
BOT_TOKEN=ваш_токен_бота_телеграм
