class Card:
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
        return self._name

    @property
    def quantity(self):
        return self._quantity

    @property
    def layout(self):
        return self._layout

    @property
    def mana_cost(self):
        return self._mana_cost

    @property
    def cmc(self):
        return self._cmc

    @property
    def type_line(self):
        return self._type_line

    @property
    def oracle_text(self):
        return self._oracle_text

    @property
    def rarity(self):
        return self._rarity

    @property
    def is_land(self):
        return self._is_land

    @property
    def is_cheap_card_draw_spell(self):
        return self._is_cheap_card_draw_spell

    @property
    def is_cheap_mana_ramp_spell(self):
        return self._is_cheap_mana_ramp_spell

    @property
    def is_land_spell_mdfc(self):
        return self._is_land_spell_mdfc
