from api.utils.parser.card import Card


class Section:
    def __init__(self, name: str, cards: list[Card]):
        self._name = name
        self._cards = cards

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards
