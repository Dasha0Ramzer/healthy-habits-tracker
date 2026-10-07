import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    if not chat_id:
        logger.warning("Не удалось отправить сообщение: отсутствует chat_id")
        return

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    try:
        response = requests.get(
            f"{settings.TELEGRAM_URL}{settings.BOT_TOKEN}/sendMessage",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка отправки в Telegram: {e}")
