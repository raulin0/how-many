class Card:
    """
    Represents a card in a collectible card game.

    Attributes:
        _name (str): The name of the card.
        _quantity (int): The quantity of copies of the card.
        _layout (str): The layout of the card.
        _mana_cost (str): The mana cost of the card.
        _cmc (float): The converted mana cost (CMC) of the card.
        _type_line (str): The type line of the card.
        _rarity (str): The rarity of the card.
        _oracle_text (str): The oracle text of the card.
        _is_land (bool): Indicates if the card is a land.
        _is_cheap_card_draw_spell (bool): Indicates if the card is a cheap card draw spell.
        _is_cheap_mana_ramp_spell (bool): Indicates if the card is a cheap mana ramp spell.
        _is_land_spell_mdfc (bool): Indicates if the card is a modal double-faced card (MDFC) that can be played as a land.
    """

    def __init__(
        self,
        name: str,
        quantity: int,
        layout: str,
        mana_cost: str,
        cmc: float,
        type_line: str,
        rarity: str,
        oracle_text: str,
        is_land: bool,
        is_cheap_card_draw_spell: bool,
        is_cheap_mana_ramp_spell: bool,
        is_land_spell_mdfc: bool,
    ):
        """
        Initializes a new instance of the Card class.

        Parameters:
            name (str): The name of the card.
            quantity (int): The quantity of copies of the card.
            layout (str): The layout of the card.
            mana_cost (str): The mana cost of the card.
            cmc (float): The converted mana cost (CMC) of the card.
            type_line (str): The type line of the card.
            rarity (str): The rarity of the card.
            oracle_text (str): The oracle text of the card.
            is_land (bool): Indicates if the card is a land.
            is_cheap_card_draw_spell (bool): Indicates if the card is a cheap card draw spell.
            is_cheap_mana_ramp_spell (bool): Indicates if the card is a cheap mana ramp spell.
            is_land_spell_mdfc (bool): Indicates if the card is a modal double-faced card (MDFC) that can be played as a land.
        """
        self._name = name
        self._quantity = quantity
        self._layout = layout
        self._mana_cost = mana_cost
        self._cmc = cmc
        self._type_line = type_line
        self._rarity = rarity
        self._oracle_text = oracle_text
        self._is_land = is_land
        self._is_cheap_card_draw_spell = is_cheap_card_draw_spell
        self._is_cheap_mana_ramp_spell = is_cheap_mana_ramp_spell
        self._is_land_spell_mdfc = is_land_spell_mdfc

    @property
    def name(self):
        """
        str: Returns the name of the card.
        """
        return self._name

    @property
    def quantity(self):
        """
        int: Returns the quantity of copies of the card.
        """
        return self._quantity

    @property
    def layout(self):
        """
        str: Returns the layout of the card.
        """
        return self._layout

    @property
    def mana_cost(self):
        """
        str: Returns the mana cost of the card.
        """
        return self._mana_cost

    @property
    def cmc(self):
        """
        float: Returns the converted mana cost (CMC) of the card.
        """
        return self._cmc

    @property
    def type_line(self):
        """
        str: Returns the type line of the card.
        """
        return self._type_line

    @property
    def oracle_text(self):
        """
        str: Returns the oracle text of the card.
        """
        return self._oracle_text

    @property
    def rarity(self):
        """
        str: Returns the rarity of the card.
        """
        return self._rarity

    @property
    def is_land(self):
        """
        bool: Indicates if the card is a land.
        """
        return self._is_land

    @property
    def is_cheap_card_draw_spell(self):
        """
        bool: Indicates if the card is a cheap card draw spell.
        """
        return self._is_cheap_card_draw_spell

    @property
    def is_cheap_mana_ramp_spell(self):
        """
        bool: Indicates if the card is a cheap mana ramp spell.
        """
        return self._is_cheap_mana_ramp_spell

    @property
    def is_land_spell_mdfc(self):
        """
        bool: Indicates if the card is a modal double-faced card (MDFC) that can be played as a land.
        """
        return self._is_land_spell_mdfc
