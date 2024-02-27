import django_filters

from api.models import Decklist


class DecklistFilter(django_filters.FilterSet):
    class Meta:
        model = Decklist
        fields = {
            'commanders_id': ['exact'],
            'companion_id': ['exact'],
            'maindeck_id': ['exact'],
            'sideboard_id': ['exact'],
        }
