# Healthy Habits Tracker

Django REST Framework проект для трекинга полезных привычек. 
Проект полностью контейнеризирован и настроен для автоматического развертывания (CI/CD).

## Технологии
- **Backend:** Python 3.12, Django, Django REST Framework (DRF)
- **База данных:** PostgreSQL 16
- **Кэш и брокер сообщений:** Redis 7
- **Асинхронные задачи:** Celery + django-celery-beat
- **Веб-сервер:** Nginx (раздача статики и проксирование) + Gunicorn
- **Авторизация:** JWT (SimpleJWT)
- **Документация:** Swagger (drf-yasg)
- **Инфраструктура:** Docker, Docker Compose, GitHub Actions

## Локальный запуск

Для запуска проекта вам понадобятся установленные **Docker** и **Docker Compose**.

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Dasha0Ramzer/healthy-habits-tracker.git
   cd healthy-habits-tracker
   ```

2. Создайте файл `.env` на основе шаблона `.env.example`:

   ```bash
   cp .env.example .env
   ```
   Заполните файл `.env` своими значениями. Для локального запуска `DEBUG` можно оставить `True`,
   а в `ALLOWED_HOSTS` указать `localhost,127.0.0.1`.

3. Запустите проект одной командой:

    ```bash
    docker compose up -d --build
    ```
    `Docker` автоматически соберет образы, применит миграции, соберет статику и запустит все сервисы.

4. Приложение будет доступно по адресам:

- Главная страница / API: http://localhost/
- Админка: http://localhost/admin/
- Swagger: http://localhost/swagger/

## Переменные окружения (.env)
Все чувствительные данные вынесены в `.env` файл.
Пример полного файла смотрите в .env.example.

- SECRET_KEY - Секретный ключ Django
- DEBUG - Режим отладки
- ALLOWED_HOSTS - Разрешенные хосты
- DATABASE_NAME - Имя базы данных PostgreSQL
- DATABASE_USER -	Пользователь базы данных
- DATABASE_PASSWORD -	Пароль к базе данных
- DB_HOST -	Хост базы данных
- CELERY_BROKER_URL -	Адрес Redis для брокера
- CELERY_RESULT_BACKEND	- Адрес Redis для результатов
- EMAIL_HOST_USER	- Почта для отправки писем
- EMAIL_HOST_PASSWORD	- Пароль приложения от почты
- BOT_TOKEN	- Токен Telegram-бота
- STRIPE_API_KEY	- Ключ API Stripe

## CI/CD и Деплой на сервер
В проекте настроен пайплайн `GitHub Actions`.

### Как это работает:
При каждом `push` или `Pull Request` в ветку `main` запускается `workflow`.

Этап 1 (test_and_lint): Проверяется код линтером `flake8` и запускаются тесты Django.

Этап 2 (build): Проверяется, что Docker-образ собирается без ошибок.

Этап 3 (deploy): Если тесты и сборка прошли успешно, проект автоматически деплоится на удаленный сервер.

### Сервер
Проект развернут на виртуальной машине в Yandex Cloud и доступен по адресу:
http://84.201.180.190/admin/

Сервер настроен на автоматический перезапуск контейнеров, поэтому при падении любого сервиса Docker поднимет его снова.

### Настройка сервера и секретов (Пошагово)

1. **Сервер (Ubuntu):**
   Установите Docker и Docker Compose:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
   sudo usermod -aG docker $USER
   ```
   Клонируйте репозиторий в папку `~/app` и создайте файл `.env` с production-настройками.

2. **Настройка SSH для деплоя:**
   
   Сгенерируйте ключ локально: `ssh-keygen -t ed25519 -f ~/.ssh/github_deploy`
   
   Публичный ключ (`~/.ssh/github_deploy.pub`) добавьте на сервер в `~/.ssh/authorized_keys`.
   
   Приватный ключ (`~/.ssh/github_deploy`) скопируйте в GitHub Secrets.

3. **Секреты в GitHub:**
В настройках репозитория добавьте:

- `SSH_HOST` — IP-адрес сервера

- `SSH_USER` — имя пользователя (например, yc-user или ramzer)

- `SSH_KEY` — приватный SSH-ключ

4. **Порты на сервере (Security Group):**
В панели Yandex Cloud должны быть открыты только необходимые порты:

- 22 (SSH) — для управления сервером и деплоя

- 80 (HTTP) — для доступа к веб-приложению

- 443 (HTTPS) — для защищенного доступа (если настроен)

## Тестирование
Запуск тестов локально:
```bash
docker compose exec web python manage.py test
```