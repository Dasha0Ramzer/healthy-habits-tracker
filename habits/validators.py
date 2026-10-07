from django.core.exceptions import ValidationError


def validate_exclusive_reward_or_related(data):
    """Нельзя одновременно указать связанную привычку и вознаграждение."""
    if data.get("related_habit") and data.get("reward"):
        raise ValidationError(
            "Можно заполнить только одно: связанную привычку или вознаграждение."
        )


def validate_related_is_pleasant(data):
    """В связанные можно добавлять только приятные привычки."""
    related = data.get("related_habit")
    if related and not related.is_pleasant:
        raise ValidationError(
            "В связанные привычки можно добавлять только приятные привычки."
        )


def validate_pleasant_has_no_reward_or_related(data):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    if data.get("is_pleasant") and (data.get("reward") or data.get("related_habit")):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )
