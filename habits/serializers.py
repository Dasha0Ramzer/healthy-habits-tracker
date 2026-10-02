from rest_framework import serializers

from .models import Habit
from .validators import (validate_exclusive_reward_or_related,
                         validate_pleasant_has_no_reward_or_related,
                         validate_related_is_pleasant)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        if self.instance:
            for field in ("is_pleasant", "reward", "related_habit"):
                if field not in data:
                    data[field] = getattr(self.instance, field)
        validate_exclusive_reward_or_related(data)
        validate_related_is_pleasant(data)
        validate_pleasant_has_no_reward_or_related(data)
        return data
