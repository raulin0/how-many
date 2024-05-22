from api.utils.parser.card import Card


class Section:
    """
    Represents a section that contains a set of cards.

    Attributes:
        _name (str): The name of the section.
        _cards (list[Card]): The list of cards contained in the section.
    """

    def __init__(self, name: str, cards: list[Card]):
        """
        Initializes a new instance of the Section class.

        Parameters:
            name (str): The name of the section.
            cards (list[Card]): The list of cards contained in the section.
        """
        self._name = name
        self._cards = cards

    @property
    def name(self):
        """
        str: Returns the name of the section.
        """
        return self._name

    @property
    def cards(self):
        """
        list[Card]: Returns the list of cards contained in the section.
        """
        return self._cards
