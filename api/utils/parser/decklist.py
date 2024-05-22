from api.utils.parser.section import Section


class Decklist:
    """
    Represents a deck list in a collectible card game.

    Attributes:
        _sections (list[Section]): The sections of the deck.
        _is_commander_deck (bool): Indicates if the deck is a Commander deck.
        _has_companion (bool): Indicates if the deck has a Companion.
        _maindeck_card_count (int): The number of cards in the maindeck.
        _non_land_card_count (int): The number of cards that are not lands.
        _non_land_cmcs_count (float): The sum of converted mana costs (CMC) of non-land cards.
        _cheap_card_draw_spell_count (int): The number of cheap card draw spells.
        _cheap_mana_ramp_spell_count (int): The number of cheap mana ramp spells.
        _non_mythic_land_spell_mdfc_count (int): The number of non-mythic modal double-faced cards (MDFC) that can be played as lands.
        _mythic_land_spell_mdfc_count (int): The number of mythic modal double-faced cards (MDFC) that can be played as lands.
        _average_cmc (float): The average converted mana cost (CMC) of the deck.
        _recommended_number_of_lands (int): The recommended number of lands in the deck.
    """

    def __init__(
        self,
        sections: list[Section],
        is_commander_deck: bool,
        has_companion: bool,
        maindeck_card_count: int,
        non_land_card_count: int,
        non_land_cmcs_count: float,
        cheap_card_draw_spell_count: int,
        cheap_mana_ramp_spell_count: int,
        non_mythic_land_spell_mdfc_count: int,
        mythic_land_spell_mdfc_count: int,
        average_cmc: float,
        recommended_number_of_lands: int,
    ):
        """
        Initializes a new instance of the Decklist class.

        Parameters:
            sections (list[Section]): The sections of the deck.
            is_commander_deck (bool): Indicates if the deck is a Commander deck.
            has_companion (bool): Indicates if the deck has a Companion.
            maindeck_card_count (int): The number of cards in the maindeck.
            non_land_card_count (int): The number of cards that are not lands.
            non_land_cmcs_count (float): The sum of converted mana costs (CMC) of non-land cards.
            cheap_card_draw_spell_count (int): The number of cheap card draw spells.
            cheap_mana_ramp_spell_count (int): The number of cheap mana ramp spells.
            non_mythic_land_spell_mdfc_count (int): The number of non-mythic modal double-faced cards (MDFC) that can be played as lands.
            mythic_land_spell_mdfc_count (int): The number of mythic modal double-faced cards (MDFC) that can be played as lands.
            average_cmc (float): The average converted mana cost (CMC) of the deck.
            recommended_number_of_lands (int): The recommended number of lands in the deck.
        """
        self._sections = sections
        self._is_commander_deck = is_commander_deck
        self._has_companion = has_companion
        self._maindeck_card_count = maindeck_card_count
        self._non_land_card_count = non_land_card_count
        self._non_land_cmcs_count = non_land_cmcs_count
        self._cheap_card_draw_spell_count = cheap_card_draw_spell_count
        self._cheap_mana_ramp_spell_count = cheap_mana_ramp_spell_count
        self._non_mythic_land_spell_mdfc_count = (
            non_mythic_land_spell_mdfc_count
        )
        self._mythic_land_spell_mdfc_count = mythic_land_spell_mdfc_count
        self._average_cmc = average_cmc
        self._recommended_number_of_lands = recommended_number_of_lands

    @property
    def sections(self):
        """
        list[Section]: Returns the sections of the deck.
        """
        return self._sections

    @property
    def is_commander_deck(self):
        """
        bool: Indicates if the deck is a Commander deck.
        """
        return self._is_commander_deck

    @property
    def has_companion(self):
        """
        bool: Indicates if the deck has a Companion.
        """
        return self._has_companion

    @property
    def maindeck_card_count(self):
        """
        int: Returns the number of cards in the maindeck.
        """
        return self._maindeck_card_count

    @property
    def non_land_card_count(self):
        """
        int: Returns the number of cards that are not lands.
        """
        return self._non_land_card_count

    @property
    def non_land_cmcs_count(self):
        """
        float: Returns the sum of converted mana costs (CMC) of non-land cards.
        """
        return self._non_land_cmcs_count

    @property
    def cheap_card_draw_spell_count(self):
        """
        int: Returns the number of cheap card draw spells.
        """
        return self._cheap_card_draw_spell_count

    @property
    def cheap_mana_ramp_spell_count(self):
        """
        int: Returns the number of cheap mana ramp spells.
        """
        return self._cheap_mana_ramp_spell_count

    @property
    def non_mythic_land_spell_mdfc_count(self):
        """
        int: Returns the number of non-mythic modal double-faced cards (MDFC) that can be played as lands.
        """
        return self._non_mythic_land_spell_mdfc_count

    @property
    def mythic_land_spell_mdfc_count(self):
        """
        int: Returns the number of mythic modal double-faced cards (MDFC) that can be played as lands.
        """
        return self._mythic_land_spell_mdfc_count

    @property
    def average_cmc(self):
        """
        float: Returns the average converted mana cost (CMC) of the deck.
        """
        return self._average_cmc

    @property
    def recommended_number_of_lands(self):
        """
        int: Returns the recommended number of lands in the deck.
        """
        return self._recommended_number_of_lands
